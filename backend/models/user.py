from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator
from datetime import datetime, date
from fastapi import HTTPException
import re


class AppUser(SQLModel, table=True):
    """Create an SQLModel for users"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    first_name: str
    last_name: str
    email: str
    role_id: int
    team_id: Optional[int] = None
    start_date: date
    created_at: datetime
    updated_at: datetime
    is_active: bool

    __table_args__ = {"schema": "app_db"}

    @validator("first_name", always=True)
    def valid_first_name(cls, first_name):
        assert first_name.replace(
            " ", ""
        ).isalpha(), "only alphabet letters allowed in first name"
        if first_name[0].isupper() == False:
            raise HTTPException(
                status_code=400, detail="first name should start with a capital letter"
            )
        return first_name

    @validator("last_name", always=True)
    def valid_last_name(cls, ln_input):
        assert ln_input.replace(
            " ", ""
        ).isalpha(), "only alphabet letters allowed in last name"
        return ln_input

    @validator("email", always=True)
    def valid_email(cls, email_input):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        assert re.fullmatch(regex, email_input), "email format incorrect"
        return email_input
