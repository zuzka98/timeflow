from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Role(SQLModel, table=True):
    """Create an SQLModel for roles"""

    id: Optional[int] = Field(default=None, primary_key=True)
    short_name: str
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    __table_args__ = {"schema": "app_db"}
