import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog


def get_activity_list(project_name, date_from, date_to):
    activity_list = []
    total_matching = 0  # number of activities

    with SessionLocal() as db:
        try:
            query = (
                db.query(
                    Activity.name.label("activity_name"),
                    func.sum(TimeLog.hours).label("total_hours"),
                )
                .join(TimeLog, TimeLog.activity_id == Activity.id)
                .join(Project, TimeLog.project_id == Project.id)
                .filter(Project.name == project_name)
            )

            if date_from:
                date_from_obj = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
                query = query.filter(TimeLog.log_date >= date_from_obj)

            if date_to:
                date_to_obj = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
                query = query.filter(TimeLog.log_date <= date_to_obj)

            query = query.group_by(Activity.name).order_by(
                desc(func.sum(TimeLog.hours))
            )

            results = query.all()

            for row in results:
                activity_list.append(
                    {
                        "activity": row.activity_name,
                        "hours": (
                            float(round(row.total_hours, 2)) if row.total_hours else 0
                        ),
                        "users": get_user_dict(
                            project_name, row.activity_name
                        ),  # ✅ FIXED
                    }
                )

            total_matching = len(activity_list)

        except SQLAlchemyError as e:
            print(f"❌ Database error in get_activity_list: {e}", flush=True)
            activity_list = []
            total_matching = 0

    print(activity_list, total_matching, flush=True)
    return activity_list


def get_user_dict(project_name, activity_name):
    user_dict = {}

    with SessionLocal() as db:
        results = (
            db.query(
                User.name.label("user_name"),
                User.surname.label("user_surname"),
                func.sum(TimeLog.hours).label("total_hours"),
            )
            .join(TimeLog, TimeLog.user_id == User.id)
            .join(Project, TimeLog.project_id == Project.id)
            .join(Activity, TimeLog.activity_id == Activity.id)
            .filter(Project.name == project_name)
            .filter(Activity.name == activity_name)
            .group_by(User.id, User.name, User.surname)
            .all()
        )

        for row in results:
            full_name = f"{row.user_name} {row.user_surname}"
            user_dict[full_name] = (
                float(round(row.total_hours, 2)) if row.total_hours else 0
            )

    return user_dict


if __name__ == "__main__":
    projects, total = get_activity_list("171503-FD23", "2017-02-22", "2020-02-22")
    print("Activities:", projects)
    print("Total matching activities:", total)
