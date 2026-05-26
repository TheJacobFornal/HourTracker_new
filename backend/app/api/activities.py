# app/api/activities.py
from fastapi import APIRouter

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/")
def get_activities():
    # In a real scenario, you'd query your database or model here
    return [
        {"id": 1, "name": "Activity 1"},
        {"id": 2, "name": "Activity 2"},
    ]
