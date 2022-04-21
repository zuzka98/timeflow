from typing import Optional
from sqlmodel import Field, SQLModel, MetaData
from datetime import datetime


class Client(SQLModel, table=True):
    """Create an SQLModel for clients"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    __table_args__ = {"schema": "app_db"}
