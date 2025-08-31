import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog


def get_projects_list():
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


def activity_list(project_name):
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


def get_project_details(project_name):

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


# Project Details Page #
def get_activity_details(project_name, activity_name):
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


if __name__ == "__main__":
    project = "250403-CF"
    activities = activity_list(project)

    print("Activities found:", activities)

    for activity_name in activities:  # Now activity_name is a string, not a tuple
        print("\n🔍 Processing activity:", activity_name)
        details = get_activity_details(project, activity_name)

        if "error" in details:
            print(f"❌ Error: {details['error']}")
        else:
            print(f"   Total hours: {details.get('total_hours', 0):.1f}")
            print(f"   Entry count: {details.get('entry_count', 0)}")
            if details.get("first_date") and details.get("last_date"):
                print(
                    f"   Date range: {details['first_date']} to {details['last_date']}"
                )
