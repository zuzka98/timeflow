from typing import Optional
from sqlmodel import Field, SQLModel, MetaData
from datetime import datetime


class Demand(SQLModel, table=True):
    """Create an SQLModel for demands"""

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="app_db.team.id")
    epic_id: int = Field(foreign_key="app_db.epic.id")
    year: int
    month: int
    days: int
    created_at: datetime
    updated_at: datetime
    is_locked: bool = False

    __table_args__ = {"schema": "app_db"}
