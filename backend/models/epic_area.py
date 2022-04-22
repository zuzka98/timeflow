from typing import Optional
from sqlmodel import Field, SQLModel, MetaData
from datetime import datetime


class EpicArea(SQLModel, table=True):
    """Create an SQLModel for epic areas"""

    id: Optional[int] = Field(default=None, primary_key=True)
    epic_id: int = Field(foreign_key="app_db.epic.id")
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    __table_args__ = {"schema": "app_db"}
