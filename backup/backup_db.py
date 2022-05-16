from datetime import datetime, timedelta
import ftplib
import dask
import os
import pyodbc
import pandas as pd
import re


BACKUP_INTERVAL_HOURS = 6
current_datetime = datetime.now()
dt_backup_int = current_datetime - timedelta(
    hours=BACKUP_INTERVAL_HOURS
)  # subtract given hours from current datetime

# Connection string to database
cnxn = pyodbc.connect(
    "DRIVER={PostgreSQL Unicode};Server=127.0.0.1;Port=5432;Database=test_db;Uid=pguser;Pwd=password;"
)


@dask.delayed
def get_table_names() -> pd.DataFrame:
    """
    Return a Pandas DataFrame containing all table names except for calendar.
    """
    # Get all table names with app_db schema
    table_name_query = """SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'app_db'"""

    df_table_names = pd.io.sql.read_sql(table_name_query, cnxn)

    # Remove calendar from DataFrame of table names
    df_table_names = df_table_names.loc[df_table_names["table_name"] != "calendar"]
    return df_table_names


@dask.delayed
def backup_db(df_table_names: pd.DataFrame):
    """
    Backup the entire database all at once if it's the first backup, otherwise backup according to a set of time based rules.
    First backup is stored in a directory called 0000-00-00.
    Returns a dictionary containing the date that was updated and the batch number.
    """
    path = f"{os.getcwd()}\\0000-00-00"
    if not os.path.exists(path):
        # First backup
        first_backup(df_table_names)
        backup_info = {"folder_name": "0000-00-00", "batch": None}
    else:
        # Not first backup
        backup_info = update_backup(df_table_names)
    return backup_info


@dask.delayed
def cloud_backup(backup_info: dict):
    """
    Send latest backup to the cloud.

    Parameters
    ----------
    backup_info: dict
        Dictionary containing information in regards to date of backup and batch number.
    """
    session = ftplib.FTP_TLS("u301483.your-storagebox.de")
    session.login(user="u301483", passwd="dI52PgdgGeB8js0v")

    try:
        if backup_info["folder_name"] == "0000-00-00":
            path = f"{os.getcwd()}\\0000-00-00"
            file = open(path, "rb")
            session.storbinary(f"STOR {path}", file)
            file.close()

        else:
            path_to_date = f'{os.getcwd()}\\{backup_info["folder_name"]}'
            for parquet_file in os.listdir(path_to_date):
                priority = re.search(r"\d", parquet_file)
                digit = int(priority.group())
                if digit <= backup_info["batch"]:
                    path = (
                        f'{os.getcwd()}\\{backup_info["folder_name"]}\\{parquet_file}'
                    )
                    file = open(path, "rb")
                    session.storbinary(f"STOR {path}", file)
                    file.close()
    except TypeError:
        pass

    session.quit()


def first_backup(df_table_names: pd.DataFrame):
    """
    Backup the entire database all at once.
    """
    for table in df_table_names["table_name"]:
        query = f"""SELECT * 
            FROM app_db.{table}"""
        df = pd.io.sql.read_sql(query, cnxn)
        if not df.empty:
            folder_name = "0000-00-00"

            # Create folder for backup files
            try:
                os.mkdir("0000-00-00")

            except FileExistsError:
                pass
            path = f"{os.getcwd()}\\{folder_name}\\{table}0.parquet"
            df.to_parquet(path=path, compression=None)


def update_backup(df_table_names: pd.DataFrame):
    """
    Update database backup.
    Returns a dictionary the name of the folder which was backed up to and the number of the batch.
    """
    for table in df_table_names["table_name"]:
        query = query = f"""SELECT * 
            FROM app_db.{table}
            WHERE updated_at >= '{str(dt_backup_int)}'"""
        df = pd.io.sql.read_sql(query, cnxn)
        if not df.empty:
            folder_name = str(current_datetime.date())

            # Create folder for backup files
            try:
                os.mkdir(folder_name)
            except FileExistsError:
                pass
            path = f"{os.getcwd()}\\{folder_name}\\{table}0.parquet"
            batch = 0

            uniq = 1
            while os.path.exists(path):
                batch += 1
                path = f"{os.getcwd()}\\{folder_name}\\{table}{uniq}.parquet"
                uniq += 1
            df.to_parquet(path=path, compression=None)
            return {"folder_name": folder_name, "batch": batch}


tables = get_table_names()
backup = backup_db(tables)
cloud_backup = cloud_backup(backup)

cloud_backup.compute()
