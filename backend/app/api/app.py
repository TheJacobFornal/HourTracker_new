from app.scripts.Export_Data_DB import OUT_Main
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
    _root_candidates.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    )

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
from app.models.time_logs_daily import DailyLog
from app.models.user import User
from app.scripts.Export_Data_DB import Activity_Search
from app.scripts.Export_Data_DB import Projects_Search
from app.scripts.Export_Excel import Export_To_Excel
from datetime import datetime
from fastapi.responses import StreamingResponse


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


from sqlalchemy import func


@app.post("/api/project/header_info")
def header_info(payload: dict, db: Session = Depends(get_db)):
    project_name = payload.get("project_name")

    if not project_name:
        raise HTTPException(status_code=400, detail="Missing project_name")

    try:
        # Aggregate both TimeLog and DailyLog
        row = (
            db.query(
                Project.name.label("project_name"),
                Project.status.label("status"),
                User.name.label("leader_name"),
                User.surname.label("leader_surname"),
                func.min(func.coalesce(TimeLog.log_date, DailyLog.log_date)).label(
                    "date_from"
                ),
                func.max(func.coalesce(TimeLog.log_date, DailyLog.log_date)).label(
                    "date_to"
                ),
                (
                    func.coalesce(func.sum(TimeLog.hours), 0)
                    + func.coalesce(func.sum(DailyLog.hours), 0)
                ).label("total_hours"),
            )
            .outerjoin(TimeLog, TimeLog.project_id == Project.id)
            .outerjoin(DailyLog, DailyLog.project_id == Project.id)
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


@app.post("/api/project/activities_details")  # List with activities and users summary
def activity_details(payload: dict):
    project_name = payload.get("project_name")
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")

    final_list = OUT_Main.get_project_activities_user_json(
        project_name, date_from, date_to
    )

    return final_list


@app.post("/api/project/export_excel")
def export_to_excel(payload: dict):
    project_name = payload.get("project_name")
    excel_file = Export_To_Excel.main(project_name)
    filename = f"{project_name}_{datetime.now().strftime('%Y-%m-%d')}_HourTracker.xlsx"
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/")
def home(request: Request):
    url = request.url
    host = url.hostname or "unknown"
    scheme = url.scheme or "http"
    port = url.port or (443 if scheme == "https" else 80)
    message = f"Hello 06 10, FastAPI is running at {scheme}://{host}:{port}!"
    print(f"Received request for home from {scheme}://{host}:{port}", flush=True)
    return {"message": message}


@app.get("/version")
def version():
    version = "4.0.0"
    data_realse = "30.01.26"
    return {"version": version, "data_realse": data_realse}


@app.post("/api/activities/by_month")
def activities_by_month(payload: dict, db: Session = Depends(get_db)):
    month = payload.get("month")
    year = payload.get("year")
    if not month or not year:
        raise HTTPException(status_code=400, detail="Missing month or year")

    import datetime
    from app.models.activity import Activity

    date_from = datetime.date(year, month, 1)
    # exclusive upper bound — same as SQL: log_date < first day of next month
    if month == 12:
        date_to_excl = datetime.date(year + 1, 1, 1)
    else:
        date_to_excl = datetime.date(year, month + 1, 1)

    rows = (
        db.query(
            Activity.id,
            Activity.name,
            Activity.description,
            Activity.team_id,
        )
        .join(TimeLog, TimeLog.activity_id == Activity.id)
        .filter(TimeLog.log_date >= date_from, TimeLog.log_date < date_to_excl)
        .distinct()
        .order_by(Activity.name)
        .all()
    )

    activities = [
        {"id": r.id, "name": r.name, "description": r.description, "team_id": r.team_id}
        for r in rows
    ]
    return {"activities": activities}


@app.post("/api/zestawienie/export_excel")
def zestawienie_export_excel(payload: dict):
    month = payload.get("month")
    year = payload.get("year")
    activity_ids = payload.get("activity_ids", [])
    if not month or not year or not activity_ids:
        raise HTTPException(status_code=400, detail="Missing month, year or activity_ids")

    from app.scripts.Export_Excel.Export_Zestawienie import generate
    import datetime
    stream = generate(month, year, activity_ids)
    month_str = datetime.date(year, month, 1).strftime("%Y-%m")
    filename = f"Zestawienie_{month_str}.xlsx"
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/get/leaders")
def get_leaders():
    print("Received request for leaders", flush=True)
    leaders = ["Mariusz", "Rafal", "Zbyszek"]
    return leaders


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="10.1.69.13", port=8000)
