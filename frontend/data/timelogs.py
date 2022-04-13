import requests
import json
from typing import List, Dict, TypedDict
from data.common import Select
from config import base_url


class Timelog(TypedDict):
    start_time: str
    end_time: str
    user_id: int
    epic_id: int
    count_hours: float
    count_days: float
    month: int
    year: int


def to_timelog(
    start_time: str,
    end_time: str,
    user_id: int,
    epic_id: int,
    count_hours: float,
    count_days: float,
    month: int,
    year: int,
) -> bool:
    data = Timelog(
        start_time=start_time,
        end_time=end_time,
        user_id=user_id,
        epic_id=epic_id,
        count_hours=0,
        count_days=0,
        month=str(month),
        year=str(year),
    )
    response = requests.post(
        f"{base_url}/api/timelogs",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def timelog_by_user_epic_year_month(user_id, epic_id, year, month) -> List[Dict]:
    if user_id != "" and epic_id != "" and year != "" and month != "":
        api = f"{base_url}/api/timelogs/users/{user_id}/epics/{epic_id}"
        params = {"year": year, "month": month}
        response = requests.get(api, params=params)
        rows = []
        for item in response.json():
            d = {
                "timelog id": item["id"],
                "username": item["username"],
                "epic name": item["epic_name"],
                "start time": (item["start_time"]).replace("T", " "),
                "end time": (item["end_time"]).replace("T", " "),
                "count hours": item["count_hours"],
                "count days": item["count_days"],
            }
            rows.append(d)
        print(rows)
        return rows
