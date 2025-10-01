import uvicorn
import os
import sys

# Ensure project root is on sys.path when running as a bundled executable or script
_root_candidates = []
if getattr(sys, "frozen", False):
    _root_candidates.extend(
        [
            getattr(sys, "_MEIPASS", ""),
            os.path.dirname(sys.executable),
        ]
    )
else:
    _root_candidates.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

for candidate in _root_candidates:
    if not candidate:
        continue
    backend_path = os.path.join(candidate, "backend")
    if os.path.isdir(backend_path) and backend_path not in sys.path:
        sys.path.insert(0, backend_path)

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.project import Project
from app.models.time_log import TimeLog
from app.models.user import User
from app.scripts.Export_Data import Activity_Search
from app.scripts.Export_Data import Projects_Search


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="HourTracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/projects/search")
def search_project(payload: dict):
    users = payload.get("users", [])
    status = payload.get("status")
    leader = payload.get("leader")
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")
    date_order = payload.get("date_sort")
    search = payload.get("search", "")
    page = payload.get("page", 1)
    page_size = payload.get("page_size", 51)

    print(
        "pro",
        users,
        status,
        leader,
        date_from,
        date_to,
        date_order,
        search,
        page,
        page_size,
        flush=True,
    )

    projects, record_counter = Projects_Search.get_projects_list(
        users, status, leader, date_from, date_to, date_order, search, page, page_size
    )

    return {"projects": projects, "record_counter": record_counter}


@app.post("/api/project/header_info")
def header_info(payload: dict, db: Session = Depends(get_db)):
    project_name = payload.get("project_name")

    if not project_name:
        raise HTTPException(status_code=400, detail="Missing project_name")

    try:
        row = (
            db.query(
                Project.name.label("project_name"),
                Project.status.label("status"),
                User.name.label("leader_name"),
                User.surname.label("leader_surname"),
                func.min(TimeLog.log_date).label("date_from"),
                func.max(TimeLog.log_date).label("date_to"),
                func.sum(TimeLog.hours).label("total_hours"),
            )
            .outerjoin(TimeLog, TimeLog.project_id == Project.id)
            .outerjoin(User, User.id == Project.leader_id)
            .filter(Project.name == project_name)
            .group_by(Project.name, Project.status, User.name, User.surname)
            .first()
        )
    except Exception as exc:
        print(f"Error fetching header info for {project_name}: {exc}", flush=True)
        raise HTTPException(
            status_code=500, detail="Failed to fetch project header info"
        ) from exc

    if not row:
        raise HTTPException(status_code=404, detail="Project not found")

    leader_parts = [part for part in [row.leader_name, row.leader_surname] if part]
    leader = " ".join(leader_parts) if leader_parts else "Brak lidera"

    return {
        "project": row.project_name,
        "leader": leader,
        "status": row.status or "Nieznany",
        "dateFrom": row.date_from.isoformat() if row.date_from else None,
        "dateTo": row.date_to.isoformat() if row.date_to else None,
        "totalHours": float(row.total_hours) if row.total_hours is not None else 0.0,
    }


@app.post("/api/project/activities_details")
def activity_details(payload: dict):
    project_name = payload.get("project_name")
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")

    print("activity date from:", date_from)

    activity_list = Activity_Search.get_activity_list(project_name, date_from, date_to)

    print(project_name, date_from, date_to, flush=True)

    return activity_list


@app.get("/api/projects/test")
def project_test():
    example_project1 = {
        "id": "IX_215323",
        "hours": 5100,
        "user": "Eryk Kr�likowski",
        "dateRange": "2025-05-22 to 2025-07-31",
    }

    example_project2 = {
        "id": "IX_215323",
        "hours": 55,
        "user": "Eryk Kr�likowski",
        "dateRange": "2025-05-22 to 2025-07-31",
    }

    return [example_project1, example_project2]


@app.get("/get/leaders")
def get_leaders():
    print("Received request for leaders", flush=True)
    leaders = ["Mariusz", "Rafal", "Zbyszek"]
    return leaders


@app.get("/")
def home(request: Request):
    url = request.url
    host = url.hostname or "unknown"
    scheme = url.scheme or "http"
    port = url.port or (443 if scheme == "https" else 80)
    message = f"Hello, FastAPI is running at {scheme}://{host}:{port}!"
    print(f"Received request for home from {scheme}://{host}:{port}", flush=True)
    return {"message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
