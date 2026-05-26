# app/api/projects.py
from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def get_projects():
    return [{"id": 1, "name": "Project 1"}, {"id": 2, "name": "Project 2"}]
