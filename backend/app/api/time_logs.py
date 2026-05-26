# app/api/time_logs.py
from fastapi import APIRouter

router = APIRouter(prefix="/time-logs", tags=["time_logs"])


@router.get("/")
def get_time_logs():
    # Sample data for time logs
    return [
        {"id": 1, "user_id": 1, "hours": 5, "date": "2026-01-30"},
        {"id": 2, "user_id": 2, "hours": 3, "date": "2026-01-30"},
    ]
