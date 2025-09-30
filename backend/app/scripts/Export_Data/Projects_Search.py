import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc, and_

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog


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
            .outerjoin(User, User.id == Project.leader_id)
            .filter(Project.name == project_name)
            .group_by(Project.id, Project.name, User.name, User.surname)
            .first()
        )

        if result:
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

        return project


def get_projects_list(
    users, status, leader, date_from, date_to, date_order, search, page=1, page_size=50
):
    projects_list = []
    total_matching = 0  # variable to store count of matching rows

    with SessionLocal() as db:
        try:
            base_query = (
                db.query(Project)
                .join(TimeLog)
                .group_by(
                    Project.id,
                    Project.name,
                    Project.client_id,
                    Project.leader_id,
                    Project.status,
                    Project.created_at,
                )
            )

            # Apply search filter
            if search and len(search) > 0:
                base_query = base_query.filter(Project.name.ilike(f"%{search}%"))

            # Apply filters
            if date_from and date_to:
                base_query = base_query.having(
                    func.min(TimeLog.log_date) >= date_from
                ).having(func.max(TimeLog.log_date) <= date_to)
            elif date_from:
                base_query = base_query.having(func.min(TimeLog.log_date) >= date_from)
            elif date_to:
                base_query = base_query.having(func.max(TimeLog.log_date) <= date_to)

            # Get count ignoring the limit
            total_matching = base_query.count()

            # Pagination
            offset = (page - 1) * page_size

            # Apply ordering and limit for fetching actual rows
            if date_order == "begin":
                query = base_query.order_by(func.min(TimeLog.log_date).asc())
            elif date_order == "end":
                query = base_query.order_by(func.max(TimeLog.log_date).desc())
            else:
                query = base_query.order_by(func.max(TimeLog.log_date).asc())

            query = query.offset(offset).limit(page_size)

            result = query.all()

            for row in result:
                project = get_project_details(row.name)
                projects_list.append(project)

            print("Total matching rows:", total_matching, flush=True)
            return projects_list, total_matching

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in project_list:", str(e))
            raise


if __name__ == "__main__":
    projects = get_projects_list([], None, None, "2017-02-22", "2020-02-22", "")
    print(projects)
