from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, date


class Epic(SQLModel, table=True):
    """Create an SQLModel for epic entity"""

    id: Optional[int] = Field(default=None, primary_key=True)
    short_name: str
    name: str
    team_id: int = Field(foreign_key="app_db.team.id")
    sponsor_id: int = Field(foreign_key="app_db.sponsor.id")
    start_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime

    __table_args__ = {"schema": "app_db"}
