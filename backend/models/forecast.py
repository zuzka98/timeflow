from typing import Optional
from sqlmodel import Field, SQLModel, MetaData
from pydantic import validator
from datetime import datetime
import numpy as np


class Forecast(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="app_db.appuser.id")
    epic_id: int = Field(foreign_key="app_db.epic.id")
    days: float
    month: int
    year: int

    __table_args__ = {"schema": "app_db"}

    @validator("days")
    def valid_days(cls, days_input):
        assert days_input in np.arange(
            0, 24, 0.1
        ), "Work days cannot be greater than 24"
        return days_input

    @validator("year")
    def valid_year(cls, year_input):
        assert year_input >= datetime.now().year
        return year_input
