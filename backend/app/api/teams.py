# app/api/teams.py
from fastapi import APIRouter

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/")
def get_teams():
    # Sample data for teams
    return [
        {"id": 1, "name": "Team 1"},
        {"id": 2, "name": "Team 2"},
    ]
