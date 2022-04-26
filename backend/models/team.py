from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Team(SQLModel, table=True):
    """Create an SQLModel for teams"""

    id: Optional[int] = Field(default=None, primary_key=True)
    lead_user_id: int = Field(foreign_key="app_db.appuser.id")
    name: str
    short_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    __table_args__ = {"schema": "app_db"}
