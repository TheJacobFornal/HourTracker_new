import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc, or_

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog
from app.models.time_logs_daily import DailyLog  # ✅ Daily logs


def get_project_details(project_name):
    """Return project details, summing both time_logs and daily_logs, and computing date range across both tables."""

    with SessionLocal() as db:
        # --- Aggregate time_logs ---
        time_log_agg = (
            db.query(
                func.coalesce(func.sum(TimeLog.hours), 0).label("time_hours"),
                func.min(TimeLog.log_date).label("first_time_log"),
                func.max(TimeLog.log_date).label("last_time_log"),
            )
            .join(Project, TimeLog.project_id == Project.id)
            .filter(Project.name == project_name)
            .first()
        )

        # --- Aggregate daily_logs ---
        daily_log_agg = (
            db.query(
                func.coalesce(func.sum(DailyLog.hours), 0).label("daily_hours"),
                func.min(DailyLog.log_date).label("first_daily_log"),
                func.max(DailyLog.log_date).label("last_daily_log"),
            )
            .join(Project, DailyLog.project_id == Project.id)
            .filter(Project.name == project_name)
            .first()
        )

        # --- Get project leader ---
        leader = (
            db.query(User.name, User.surname)
            .join(Project, User.id == Project.leader_id)
            .filter(Project.name == project_name)
            .first()
        )

        if not time_log_agg and not daily_log_agg:
            return None

        # --- Compute leader name ---
        leader_name = (
            f"{leader.name} {leader.surname}" if leader else "Lider nie przypisany"
        )

        # --- Sum hours ---
        total_time_hours = round(time_log_agg.time_hours if time_log_agg else 0, 2)
        total_daily_hours = round(daily_log_agg.daily_hours if daily_log_agg else 0, 2)

        # --- Determine first and last date across both tables ---
        dates = [
            d
            for d in [
                time_log_agg.first_time_log if time_log_agg else None,
                time_log_agg.last_time_log if time_log_agg else None,
                daily_log_agg.first_daily_log if daily_log_agg else None,
                daily_log_agg.last_daily_log if daily_log_agg else None,
            ]
            if d is not None
        ]
        date_range = f"{min(dates)} to {max(dates)}" if dates else ""

        project = {
            "id": project_name,
            "hours": int(round(total_time_hours)),
            "daily_hours": int(round(total_daily_hours)),
            "user": leader_name,
            "dateRange": date_range,
        }

        return project


def get_projects_list(
    users,
    status,
    leader,
    date_from,
    date_to,
    date_order,
    search,
    page=1,
    page_size=50,
):
    """Return list of projects including projects with only daily_logs."""

    projects_list = []
    total_matching = 0

    with SessionLocal() as db:
        try:
            # --- Base query: LEFT JOIN both time_logs and daily_logs ---
            base_query = (
                db.query(Project)
                .outerjoin(TimeLog, TimeLog.project_id == Project.id)
                .outerjoin(DailyLog, DailyLog.project_id == Project.id)
                .group_by(
                    Project.id,
                    Project.name,
                    Project.client_id,
                    Project.leader_id,
                    Project.status,
                    Project.created_at,
                )
            )

            # --- Filters ---
            if search:
                base_query = base_query.filter(Project.name.ilike(f"%{search}%"))

            if date_from and date_to:
                base_query = base_query.having(
                    func.coalesce(
                        func.min(TimeLog.log_date), func.min(DailyLog.log_date)
                    )
                    >= date_from
                ).having(
                    func.coalesce(
                        func.max(TimeLog.log_date), func.max(DailyLog.log_date)
                    )
                    <= date_to
                )
            elif date_from:
                base_query = base_query.having(
                    func.coalesce(
                        func.min(TimeLog.log_date), func.min(DailyLog.log_date)
                    )
                    >= date_from
                )
            elif date_to:
                base_query = base_query.having(
                    func.coalesce(
                        func.max(TimeLog.log_date), func.max(DailyLog.log_date)
                    )
                    <= date_to
                )

            # --- Total count ---
            total_matching = base_query.count()

            # --- Pagination & ordering ---
            offset = (page - 1) * page_size
            if date_order == "begin":
                query = base_query.order_by(
                    func.coalesce(
                        func.min(TimeLog.log_date), func.min(DailyLog.log_date)
                    ).asc()
                )
            elif date_order == "end":
                query = base_query.order_by(
                    func.coalesce(
                        func.max(TimeLog.log_date), func.max(DailyLog.log_date)
                    ).desc()
                )
            else:
                query = base_query.order_by(
                    func.coalesce(
                        func.max(TimeLog.log_date), func.max(DailyLog.log_date)
                    ).asc()
                )

            query = query.offset(offset).limit(page_size)
            result = query.all()

            # --- Build project details list ---
            for row in result:
                project = get_project_details(row.name)
                if project:
                    projects_list.append(project)

            return projects_list, total_matching

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in project_list:", str(e))
            raise


if __name__ == "__main__":
    projects, total = get_projects_list(
        [], None, None, "2017-02-22", "2020-02-22", "end"
    )
    print("Projects:", projects)
    print("Total:", total)
