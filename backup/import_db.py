"""
Script is to be run with backup folders and parquet files within the same directory as this script.
Importing directly from cloud has not yet been implemented.
"""

import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import re
from sqlalchemy import create_engine


load_dotenv()
POSTGRE_USER = os.getenv("POSTGRE_USER")
POSTGRE_PASS = os.getenv("POSTGRE_PASS")
POSTGRE_DB = os.getenv("POSTGRE_DB")
POSTGRE_PORT = os.getenv("POSTGRE_PORT")

# Connection to database
# cnxn = pyodbc.connect('DRIVER={PostgreSQL Unicode};Server=127.0.0.1;Port=5432;Database=test_db;Uid=pguser;Pwd=password;')
engine = create_engine(
    f"postgresql://{POSTGRE_USER}:{POSTGRE_PASS}@127.0.0.1:{POSTGRE_PORT}/{POSTGRE_DB}"
)
cnxn = engine.connect()

# Order of which to update database by
TABLE_ORDER = {
    "appuser": 0,
    "client": 1,
    "team": 2,
    "sponsor": 3,
    "epic": 4,
    "epicarea": 5,
    "role": 6,
    "rate": 7,
    "timelog": 8,
    "forecast": 9,
    "capacity": 10,
    "demand": 11,
}
REV_TABLE_ORDER = {
    "demand": 0,
    "capacity": 1,
    "forecast": 2,
    "timelog": 3,
    "rate": 4,
    "role": 5,
    "epicarea": 6,
    "epic": 7,
    "sponsor": 8,
    "team": 9,
    "client": 10,
    "appuser": 11,
}


def get_date_folders():
    """
    Return a list of the directories used for backing up the database.
    """
    directories_in_curdir = list(filter(os.path.isdir, os.listdir(os.getcwd())))
    date_folders = [
        d for d in directories_in_curdir if re.match(r"([0-9]+(-[0-9]+)+)", d)
    ]
    return date_folders


def get_parquet_files(date: str):
    """
    Return a list of the parquet files for the given date.

    Parameters
    ----------
    date : str
        Date of which to pull parquet files from. Must be in format of YYYY-MM-DD.
    """
    parquet_files = os.listdir(f"{os.getcwd()}\\{date}")
    return parquet_files


def get_file_hours_by_date(path: str):
    """
    Return a list containing the hours on which files were modified within the directory given by the path.

    Parameters
    ----------
    path : str
        Path that leads to the directory from which to pull the times from.
    """
    files = os.listdir(path)
    epoch_times = [os.path.getmtime(f"{path}\\{file}") for file in files]
    datetimes = [
        datetime.datetime.fromtimestamp(epoch_time) for epoch_time in epoch_times
    ]
    hours = [datetime.hour for datetime in datetimes]
    unique_hours = list(dict.fromkeys(hours))
    return unique_hours


def user_date_input():
    """
    Return a dictionary containing the user's chosen date and time of restore.
    """
    while True:
        try:
            print("Listing dates of all save files:")
            date_folders = get_date_folders()
            print(*date_folders, sep="\n")

            date = input(
                "Please enter the date from which you wish to restore the database from: "
            )
            date_path = f"{os.getcwd()}\\{date}"
            unique_hours = get_file_hours_by_date(date_path)
        except FileNotFoundError as e:
            print("Date entered is not valid. Please try again.")
            continue
        else:
            print(f"Listing hours for {date}:")
            print(*unique_hours, sep="\n")
            hour = input(
                "Please enter the hour from which you wish to restore the database from: "
            )
            return {"date": date, "hour": hour}


def order_parquet_files_into_batches(parquet_files):
    """
    Order the parquet files by searching for a digit within their name.
    Returns the parquet files without their numbering or extension.

    Parameters
    ----------
    parquet_files : List
        List of parquet files to be ordered.
    """
    ordered_files = {}
    for parquet_file in parquet_files:
        match_digit = re.search(r"\d", parquet_file)
        match_table = re.search(r"[a-zA-Z]+", parquet_file)
        digit = int(match_digit.group())
        table = match_table.group()
        if ordered_files.get(digit) == None:
            ordered_files[digit] = [
                table,
            ]
        else:
            ordered_files[digit].append(table)
    return ordered_files


def order_parquet_batches_by_table_order(parquet_batches):
    """
    Order the parquet batches by the specific table order.
    Returns dictionary of parquet batches that are ordered.

    Parameters
    ----------
    parquet_batches : dict
        Dictionary of parquet files to be ordered.
    """
    index = 0
    while parquet_batches.get(index) is not None:
        parquet_batch = parquet_batches[index]
        ordered_parquet_batch = sorted(parquet_batch, key=lambda x: TABLE_ORDER[x])
        parquet_batches[index] = ordered_parquet_batch
        index += 1
    return parquet_batches


def update_tables(path: str, priority: int, tables):
    """
    Update tables for a given date.

    Parameters
    ----------
    date: str
        Date from which to restore.
    priority: int
        Priority of the table to be updated. Used for creating the path to the parquet file.
    tables: list
        List of tables that need to be updated.
    """

    # Iterate over tables
    for table in tables:
        table_path = f"{path}{table}{priority}.parquet"
        df = pd.io.parquet.read_parquet(table_path)
        df.to_sql(
            name=table, schema="app_db", con=cnxn, index=False, if_exists="append"
        )
        # cnxn.commit()


def update_db_by_date(
    date_folder: str, date: str, hour: str, is_last_date: bool = False
):
    """
    Parse through the parquet files within the given directory and update the database.

    Parameters
    ----------
    date_folder: str
         Name of directory from which to pull the times from.
    date: str
        Most recent date to restore to.
    hour: str
        Most recent hour to restore to.
    is_last_date: bool
        Specifies whether the date is the last date to be updated to.
    """
    parquet_files = get_parquet_files(date_folder)
    parquet_batches = order_parquet_files_into_batches(parquet_files)
    ordered_parquet_batches = order_parquet_batches_by_table_order(parquet_batches)

    if is_last_date == True:
        # Remove parquet files if they were created after the last hour
        hours = get_file_hours_by_date(f"{os.getcwd()}\\{date_folder}")
        hours = [h for h in hours if h <= hour]
        max_batch = len(hours) - 1

        # Create list of keys to delete
        keys = []
        for key in ordered_parquet_batches.keys():
            if key > max_batch:
                keys.append(key)

        # Remove keys
        for key in keys:
            del ordered_parquet_batches[key]

    index = 0
    while ordered_parquet_batches.get(index) is not None:
        path = f"{os.getcwd()}\\{date_folder}\\"
        priority = index
        tables = ordered_parquet_batches.get(index)
        update_tables(path, priority, tables)
        index += 1


def delete_table_records():
    """
    Delete all records from all tables.
    """
    table_name_query = """SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'app_db'"""

    df_table_names = pd.io.sql.read_sql(table_name_query, cnxn)

    # Remove calendar from DataFrame of table names
    df_table_names = df_table_names.loc[df_table_names["table_name"] != "calendar"]

    list_table_names = df_table_names["table_name"].tolist()
    sorted_list_table_names = sorted(list_table_names, key=lambda x: REV_TABLE_ORDER[x])

    for table in sorted_list_table_names:
        query = f"""DELETE FROM app_db.{table}"""
        pd.io.sql.execute(query, cnxn)
        # cnxn.commit()


def restore_database():
    """
    Restore database to a specific date and time.
    """
    date, hour = user_date_input()

    # Delete all records before restoring
    delete_table_records()

    # Get date(s)
    date_folders = get_date_folders()

    for date_folder in date_folders:
        if date == date_folder:
            update_db_by_date(date_folder, date, hour, is_last_date=True)
            break
        update_db_by_date(date_folder, date, hour)


restore_database()
