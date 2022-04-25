from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Calendar(SQLModel, table=True):
    """Create an SQLModel for a calendar"""

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    year_number: int
    year_name: str
    quarter_number: int
    quarter_name: str
    month_number: int
    month_name: str
    week_number: int
    week_name: str
    week_day_number: int
    week_day_name: str

    __table_args__ = {"schema": "app_db"}
