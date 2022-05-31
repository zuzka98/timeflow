"""
Run this backup script locally.
Must be run from within the same directory that the script lies in to trigger proper file organization
"""

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv
import ftplib
import dask
import os
import pandas as pd
import re


# Load in all environment variables from .env in home directory
load_dotenv()
POSTGRE_USER = os.getenv("POSTGRE_USER")
POSTGRE_PASS = os.getenv("POSTGRE_PASS")
POSTGRE_DB = os.getenv("POSTGRE_DB")
POSTGRE_PORT = os.getenv("POSTGRE_PORT")
STORAGE_BOX_URL = os.getenv("STORAGE_BOX_URL")
STORAGE_BOX_USER = os.getenv("STORE_BOX_USER")
STORAGE_BOX_PASS = os.getenv("STORAGE_BOX_PASS")

BACKUP_INTERVAL_HOURS = 6
current_datetime = datetime.now()
dt_backup_int = current_datetime - timedelta(
    hours=BACKUP_INTERVAL_HOURS
)  # subtract given hours from current datetime

# Connection string to database
engine = create_engine(
    f"postgresql://{POSTGRE_USER}:{POSTGRE_PASS}@127.0.0.1:{POSTGRE_PORT}/{POSTGRE_DB}"
)
cnxn = engine.connect()

# Set current working directory
if os.name == "posix":
    cwd = os.getcwd()
elif os.name == "nt":
    cwd = os.getcwd().replace("\\", "/")


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
    path = f"{cwd}/0000-00-00"
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
        folder_name = backup_info["folder_name"]

        if folder_name == "0000-00-00":
            for parquet_file in os.listdir("0000-00-00"):
                path = f"{cwd}/0000-00-00/{parquet_file}"
                file = open(path, "rb")
                session.storbinary(f"STOR {folder_name}\\{parquet_file}", file)
                file.close()

        else:
            path_to_date = f"{cwd}/{folder_name}"
            for parquet_file in os.listdir(path_to_date):
                priority = re.search(r"\d", parquet_file)
                digit = int(priority.group())
                if digit <= backup_info["batch"]:
                    path = f"{cwd}/{folder_name}/{parquet_file}"
                    file = open(path, "rb")
                    session.storbinary(f"STOR {folder_name}\\{parquet_file}", file)
                    file.close()
    except TypeError:
        pass

    session.quit()
    return "Backup completed"


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
            path = f"{cwd}/{folder_name}/{table}0.parquet"
            df.to_parquet(path=path, compression=None)


def update_backup(df_table_names: pd.DataFrame):
    """
    Update database backup.
    Returns a dictionary the name of the folder which was backed up to and the number of the batch.
    """
    folder_name = ""
    date_now = str(current_datetime.date())
    batch = get_latest_batch_number(f"{cwd}/{date_now}") + 1

    # Iterate over all database tables
    for table in df_table_names["table_name"]:
        query = query = f"""SELECT * 
            FROM app_db.{table}
            WHERE updated_at >= '{str(dt_backup_int)}'"""
        df = pd.io.sql.read_sql(query, cnxn)

        # If changes were made
        if not df.empty:
            folder_name = str(current_datetime.date())

            # Create folder for backup files
            try:
                os.mkdir(folder_name)
            except FileExistsError:
                pass

            # Create path to new parquet file
            path = f"{cwd}/{folder_name}/{table}{batch}.parquet"
            df.to_parquet(path=path, compression=None)
    return {"folder_name": folder_name, "batch": batch}


def get_latest_batch_number(path: str):
    """
    Returns the latest batch number of the files in a directory.
    A regex query is used to pull the batch name from the file name.
    If no files exist, a value of -1 is returned.
    """
    batch = -1
    try:
        for file in os.listdir(path):
            priority = re.search(r"\d", file)
            digit = int(priority.group())
            if digit > batch:
                batch = digit
    except FileNotFoundError:
        pass
    return batch


tables = get_table_names()
backup = backup_db(tables)
cloud_backup = cloud_backup(backup)

cloud_backup.compute()
