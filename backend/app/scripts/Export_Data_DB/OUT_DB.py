import datetime
from operator import ge
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog
from app.models.time_logs_daily import DailyLog
import json
from sqlalchemy import func


def get_projects_list():  # list with all projects from DB
    with SessionLocal() as db:
        try:
            result = (
                db.query(Project.name)
                .group_by(Project.name, Project.created_at)  # ensures ORDER BY works
                .order_by(Project.created_at.desc())
                .limit(20)
                .all()
            )

            projects_list = [row.name for row in result]  # Only keep the name
            return projects_list

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in project_list:", str(e))
            raise


def activity_list(project_name):  # list with all activities for given project from DB
    with SessionLocal() as db:
        try:
            result = (
                db.query(Activity.name)
                .join(TimeLog, TimeLog.activity_id == Activity.id)
                .join(Project, Project.id == TimeLog.project_id)
                .filter(Project.name == project_name)
                .distinct()
                .all()
            )

            return [activity[0] for activity in result]

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in activity_list:", str(e))
            raise


def get_project_details(project_name):  # project detials for GAllery Page

    with SessionLocal() as db:
        # Query project info + aggregation
        result = (
            db.query(
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                User.name.label("leader_name"),
                User.surname.label("leader_surname"),
                func.sum(TimeLog.hours).label("total_hours"),
                func.min(TimeLog.log_date).label("first_date"),
                func.max(TimeLog.log_date).label("last_date"),
            )
            .join(TimeLog, TimeLog.project_id == Project.id)
            .outerjoin(
                User, User.id == Project.leader_id
            )  # Use outer join to allow None
            .filter(Project.name == project_name)
            .group_by(Project.id, Project.name, User.name, User.surname)
            .first()
        )

        if result:
            # Set leader to "Nikt" if None
            leader_name = (
                f"{result.leader_name} {result.leader_surname}"
                if result.leader_name and result.leader_surname
                else "Lider nie przypisany"
            )

            total_hours = round(result.total_hours) if result.total_hours else 0

            project = {
                "id": result.project_name,
                "hours": float(total_hours),
                "user": leader_name,
                "dateRange": f"{result.first_date} to {result.last_date}",
            }
        else:
            project = None

        print("Project details:", project)
        return project


### Project Details Page ###
def get_activity_details(project_name, activity_name):  # Project Header Details
    with SessionLocal() as db:
        try:
            result = (
                db.query(
                    func.sum(TimeLog.hours).label("total_hours"),
                    func.count(TimeLog.id).label("entry_counter"),
                    func.min(TimeLog.log_date).label("first_date"),
                    func.max(TimeLog.log_date).label("last_date"),
                )
                .join(Project, Project.id == TimeLog.project_id)
                .join(Activity, Activity.id == TimeLog.activity_id)
                .filter(Project.name == project_name, Activity.name == activity_name)
                .first()
            )

            if result:
                total_hours, entry_count, first_date, last_date = result
                return {
                    "project": project_name,
                    "activity": activity_name,
                    "total_hours": float(total_hours) if total_hours else 0.0,
                    "entry_count": entry_count,
                    "first_date": first_date,
                    "last_date": last_date,
                }
            else:
                return {
                    "project": project_name,
                    "activity": activity_name,
                    "total_hours": 0.0,
                    "entry_count": 0,
                    "message": "No data found",
                }

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in get_activity_details:", str(e))
            return {"error": str(e)}


def search_projects(search_term: str):
    """Return list of projects whose name contains the search term."""
    with SessionLocal() as db:
        try:
            result = (
                db.query(Project)
                .filter(Project.name.ilike(f"%{search_term}%"))
                .order_by(Project.name.asc())
                .limit(20)
                .all()
            )

            return [{"name": proj.name} for proj in result]

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in search_projects:", str(e))
            return []


# User Activities List # Project Page #
def get_user_activities_list(project_id: int):
    with SessionLocal() as db:
        try:
            rows = (
                db.query(
                    User.id.label("user_id"),
                    User.name.label("name"),
                    User.surname.label("surname"),
                    Activity.name.label("activity_name"),
                    func.coalesce(func.sum(TimeLog.hours), 0).label("time_hours"),
                    func.coalesce(func.sum(DailyLog.hours), 0).label("daily_hours"),
                )
                .join(
                    TimeLog,
                    (TimeLog.user_id == User.id) & (TimeLog.project_id == project_id),
                    isouter=True,
                )
                .join(
                    DailyLog,
                    (DailyLog.user_id == User.id) & (DailyLog.project_id == project_id),
                    isouter=True,
                )
                .join(
                    Activity,
                    Activity.id
                    == func.coalesce(TimeLog.activity_id, DailyLog.activity_id),
                    isouter=True,
                )
                .filter(
                    User.id.in_(
                        db.query(TimeLog.user_id)
                        .filter(TimeLog.project_id == project_id)
                        .union(
                            db.query(DailyLog.user_id).filter(
                                DailyLog.project_id == project_id
                            )
                        )
                    )
                )
                .group_by(User.id, User.name, User.surname, Activity.name)
                .order_by(User.surname, User.name, Activity.name)
                .all()
            )

        except Exception as exc:
            print(
                f"Error fetching activity list for project {project_id}: {exc}",
                flush=True,
            )
            return []

        # ---------- Build the final list ----------
        users = {}

        for r in rows:
            uid = r.user_id

            if uid not in users:
                users[uid] = {
                    "Name_Surname": f"{r.name} {r.surname}",
                    "Logs_Hours": 0,
                    "Daily_Hours": 0,
                    "activities": [],
                }

            # accumulate totals
            users[uid]["Logs_Hours"] += float(r.time_hours or 0)
            users[uid]["Daily_Hours"] += float(r.daily_hours or 0)

            # per-activity entry
            users[uid]["activities"].append(
                {
                    "activity": r.activity_name,
                    "Logs_Hours_activity": float(r.time_hours or 0),
                    "daily_hours_activity": float(r.daily_hours or 0),
                }
            )

        return list(users.values())


def get_project_user_sumHour_list(project_name: str):
    """
    Returns a list of users with total hours rounded to one decimal place.
    """
    with SessionLocal() as db:
        try:
            project = db.query(Project).filter(Project.name == project_name).first()
            if not project:
                return []

            p_id = project.id

            # 1. Subquery for TimeLog with rounding
            # ROUND(SUM(hours), 1) handles the math at the database level
            time_sub = (
                db.query(
                    TimeLog.user_id,
                    func.round(func.sum(TimeLog.hours), 1).label("total_time"),
                )
                .filter(TimeLog.project_id == p_id)
                .group_by(TimeLog.user_id)
                .subquery()
            )

            # 2. Subquery for DailyLog with rounding
            daily_sub = (
                db.query(
                    DailyLog.user_id,
                    func.round(func.sum(DailyLog.hours), 1).label("total_daily"),
                )
                .filter(DailyLog.project_id == p_id)
                .group_by(DailyLog.user_id)
                .subquery()
            )

            # 3. Main Query
            rows = (
                db.query(
                    User.name,
                    User.surname,
                    func.coalesce(time_sub.c.total_time, 0).label("time_hours"),
                    func.coalesce(daily_sub.c.total_daily, 0).label("daily_hours"),
                )
                .outerjoin(time_sub, User.id == time_sub.c.user_id)
                .outerjoin(daily_sub, User.id == daily_sub.c.user_id)
                .filter((time_sub.c.user_id != None) | (daily_sub.c.user_id != None))
                .order_by(User.surname, User.name)
                .all()
            )

            return [
                {
                    "Name_Surname": f"{r.name} {r.surname}",
                    "Logs_Hours": float(r.time_hours),
                    "Daily_Hours": float(r.daily_hours),
                }
                for r in rows
            ]

        except Exception as exc:
            print(f"Error: {exc}")
            return []


from sqlalchemy import func, literal_column


def get_activity_hours_per_user(project_name: str):
    with SessionLocal() as db:
        try:
            # 1. Lookup project_id
            project = db.query(Project).filter(Project.name == project_name).first()
            if not project:
                return []
            p_id = project.id

            # 2. Subqueries for TimeLog and DailyLog Sums
            time_sub = (
                db.query(
                    TimeLog.user_id,
                    TimeLog.activity_id,
                    func.sum(TimeLog.hours).label("t_sum"),
                )
                .filter(TimeLog.project_id == p_id)
                .group_by(TimeLog.user_id, TimeLog.activity_id)
                .subquery()
            )

            daily_sub = (
                db.query(
                    DailyLog.user_id,
                    DailyLog.activity_id,
                    func.sum(DailyLog.hours).label("d_sum"),
                )
                .filter(DailyLog.project_id == p_id)
                .group_by(DailyLog.user_id, DailyLog.activity_id)
                .subquery()
            )

            # 3. Main Query using 1=1 for the Cross Join
            results = (
                db.query(
                    Activity.name.label("act_name"),
                    User.name.label("u_name"),
                    User.surname.label("u_surname"),
                    func.coalesce(time_sub.c.t_sum, 0).label("time_h"),
                    func.coalesce(daily_sub.c.d_sum, 0).label("daily_h"),
                )
                .select_from(User)
                # SQL Server compatible Cross Join (1=1)
                .join(Activity, literal_column("1") == 1)
                .outerjoin(
                    time_sub,
                    (User.id == time_sub.c.user_id)
                    & (Activity.id == time_sub.c.activity_id),
                )
                .outerjoin(
                    daily_sub,
                    (User.id == daily_sub.c.user_id)
                    & (Activity.id == daily_sub.c.activity_id),
                )
                # Keep only rows where at least one log exists (matching your SQL WHERE)
                .filter((time_sub.c.user_id != None) | (daily_sub.c.user_id != None))
                .order_by(Activity.name, User.surname)
                .all()
            )

            return [
                {
                    "activity_name": r.act_name,
                    "user_full_name": f"{r.u_name} {r.u_surname}",
                    "time_log_hours": float(r.time_h),
                    "daily_log_hours": float(r.daily_h),
                    "total_combined_hours": float(r.time_h + r.daily_h),
                }
                for r in results
            ]

        except Exception as e:
            print(f"Error executing query for project '{project_name}': {e}")
            return []


if __name__ == "__main__":
    project = "252001-GA14"

    data = get_activity_hours_per_user(project)

    print(json.dumps(data, indent=4, ensure_ascii=False))
