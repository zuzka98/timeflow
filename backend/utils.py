import os
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine, text
from sqlalchemy.schema import CreateSchema


def create_connection_str():
    """
    Create connection string to be used to connect to database.
    If app is ran in developer mode, test database is used.
    If app is ran in production mode, given database is used.
    """
    if os.getenv("TIMEFLOW_DEV") == "true":
        return f"postgresql://pguser:password@db:5432/test_db"
    elif os.getenv("TIMEFLOW_DEV") == "false":
        # database_loc = "/var/lib/postgresql/data"
        POSTGRE_USER = os.getenv("POSTGRE_USER")
        POSTGRE_PASS = os.getenv("POSTGRE_PASS")
        POSTGRE_DB = os.getenv("POSTGRE_DB")
        POSTGRE_PORT = os.getenv("POSTGRE_PORT")
        return f"postgresql://{POSTGRE_USER}:{POSTGRE_PASS}@db:5432/{POSTGRE_DB}"


# Create the connection string
con_str = create_connection_str()

# Create the engine to be used to enter data into the database
engine = create_engine(con_str, echo=True, pool_size=20)

def get_session():
    with Session(engine) as session:
        yield session


def create_db():
    with engine.connect() as conn:
        with conn.begin():
            if not conn.dialect.has_schema(conn, "app_db"):
                conn.execute(CreateSchema("app_db"))
                conn.commit()
                conn.close()
    SQLModel.metadata.create_all(engine)


def execute_sample_sql(session):
    """Read sample sql database and import it."""
    with open("backend/tests/sample.sql") as f:
        content = f.read()

    queries = filter(None, content.split(";\n"))
    queries = [text(query) for query in queries]

    for query in queries:
        session.exec(query)

    session.commit()
    session.expire_all()


session = Session(engine)

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users",
    },
    {
        "name": "epic",
        "description": "operations with epics",
    },
    {
        "name": "epic_area",
        "description": "operations with epic areas",
    },
    {
        "name": "team",
        "description": "operations with teams",
    },
    {
        "name": "sponsor",
        "description": "operations with sponsors",
    },
    {
        "name": "client",
        "description": "operations with clients",
    },
    {
        "name": "forecast",
        "description": "operations with forecasts",
    },
    {
        "name": "rate",
        "description": "operations with rates",
    },
    {
        "name": "timelog",
        "description": "operations with timelogs",
    },
]


def string_to_datetime(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    return date


def string_to_datetime_hm(date_string):
    date = datetime.strptime(date_string, "%H:%M")
    return date


def string_to_datetime_GMT(date_string):
    date = datetime.strptime(date_string, "%a %b %d %Y %H:%M:%S %Z%z")
    return date


def string_to_datetime_work(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def datetime_to_string(date_date):
    date_string = date_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return date_string


def time_period(time_of_start, time_of_end):
    starting_time = string_to_datetime_work(time_of_start)
    ending_time = string_to_datetime_work(time_of_end)
    working_time = ending_time - starting_time
    return working_time


def date_str_to_date(date: str):
    date_date = datetime.strptime(date, "%Y-%m-%d").date()
    return date_date


far_date = date_str_to_date("9999-12-31")
