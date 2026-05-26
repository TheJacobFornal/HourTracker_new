import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog
from app.models.time_logs_daily import DailyLog


def get_user_dict(project_name, activity_name, date_from=None, date_to=None):
    """
    Returns a dictionary of users with their total hours and daily hours,
    sorted alphabetically by name.
    """
    user_dict = {}

    with SessionLocal() as db:
        # 🔹 Get users from time_logs
        time_query = (
            db.query(
                User.id.label("user_id"),
                User.name.label("user_name"),
                User.surname.label("user_surname"),
                func.sum(TimeLog.hours).label("time_hours"),
                Project.id.label("project_id"),
                Activity.id.label("activity_id"),
            )
            .join(TimeLog, TimeLog.user_id == User.id)
            .join(Project, TimeLog.project_id == Project.id)
            .join(Activity, TimeLog.activity_id == Activity.id)
            .filter(Project.name == project_name)
            .filter(Activity.name == activity_name)
        )

        if date_from:
            time_query = time_query.filter(TimeLog.log_date >= date_from)
        if date_to:
            time_query = time_query.filter(TimeLog.log_date <= date_to)

        time_query = time_query.group_by(
            User.id, User.name, User.surname, Project.id, Activity.id
        )
        time_results = {row.user_id: row for row in time_query.all()}

        # 🔹 Get users from daily_logs
        daily_query = (
            db.query(
                User.id.label("user_id"),
                User.name.label("user_name"),
                User.surname.label("user_surname"),
                func.sum(DailyLog.hours).label("daily_hours"),
                Project.id.label("project_id"),
                Activity.id.label("activity_id"),
            )
            .join(DailyLog, DailyLog.user_id == User.id)
            .join(Project, DailyLog.project_id == Project.id)
            .join(Activity, DailyLog.activity_id == Activity.id)
            .filter(Project.name == project_name)
            .filter(Activity.name == activity_name)
        )

        if date_from:
            daily_query = daily_query.filter(DailyLog.log_date >= date_from)
        if date_to:
            daily_query = daily_query.filter(DailyLog.log_date <= date_to)

        daily_query = daily_query.group_by(
            User.id, User.name, User.surname, Project.id, Activity.id
        )
        daily_results = {row.user_id: row for row in daily_query.all()}

        # 🔹 Combine results
        all_user_ids = set(time_results.keys()) | set(daily_results.keys())
        for user_id in all_user_ids:
            time_row = time_results.get(user_id)
            daily_row = daily_results.get(user_id)

            full_name = (
                (time_row.user_name if time_row else daily_row.user_name)
                + " "
                + (time_row.user_surname if time_row else daily_row.user_surname)
            )

            user_dict[full_name] = {
                "hours": float(round(time_row.time_hours if time_row else 0, 1)),
                "daily_hours": float(
                    round(daily_row.daily_hours if daily_row else 0, 1)
                ),
            }

    # 🔹 Sort dictionary alphabetically by user name
    sorted_user_dict = dict(sorted(user_dict.items(), key=lambda x: x[0].lower()))

    return sorted_user_dict


def get_activity_list(project_name, date_from=None, date_to=None):
    """
    Returns a list of activities for a project with total hours and daily hours.
    Falls back to daily_logs if time_logs are empty.
    """
    activity_list = []
    total_matching = 0

    date_from_obj = None
    date_to_obj = None

    if date_from:
        date_from_obj = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    if date_to:
        date_to_obj = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()

    with SessionLocal() as db:
        try:
            # 🔹 Query activities from time_logs first
            query = (
                db.query(
                    Activity.name.label("activity_name"),
                    func.sum(TimeLog.hours).label("total_hours"),
                    Activity.id.label("activity_id"),
                    Project.id.label("project_id"),
                )
                .join(TimeLog, TimeLog.activity_id == Activity.id)
                .join(Project, TimeLog.project_id == Project.id)
                .filter(Project.name == project_name)
            )

            if date_from_obj:
                query = query.filter(TimeLog.log_date >= date_from_obj)
            if date_to_obj:
                query = query.filter(TimeLog.log_date <= date_to_obj)

            query = query.group_by(Activity.id, Activity.name, Project.id).order_by(
                Activity.name.asc()
            )
            results = query.all()

            # 🔹 Add activities from time_logs
            for row in results:
                daily_query = (
                    db.query(func.sum(DailyLog.hours))
                    .filter(DailyLog.project_id == row.project_id)
                    .filter(DailyLog.activity_id == row.activity_id)
                )

                if date_from_obj:
                    daily_query = daily_query.filter(DailyLog.log_date >= date_from_obj)
                if date_to_obj:
                    daily_query = daily_query.filter(DailyLog.log_date <= date_to_obj)

                daily_hours = daily_query.scalar() or 0

                activity_list.append(
                    {
                        "activity": row.activity_name,
                        "hours": float(round(row.total_hours or 0, 1)),
                        "daily_hours": float(round(daily_hours, 1)),
                        "users": get_user_dict(
                            project_name, row.activity_name, date_from_obj, date_to_obj
                        ),
                    }
                )

            # 🔹 If no results in time_logs, fallback to daily_logs
            daily_results = (
                db.query(
                    Activity.name.label("activity_name"),
                    func.sum(DailyLog.hours).label("daily_hours"),
                    Activity.id.label("activity_id"),
                    Project.id.label("project_id"),
                )
                .join(DailyLog, DailyLog.activity_id == Activity.id)
                .join(Project, DailyLog.project_id == Project.id)
                .filter(Project.name == project_name)
            )

            if date_from_obj:
                daily_results = daily_results.filter(DailyLog.log_date >= date_from_obj)
            if date_to_obj:
                daily_results = daily_results.filter(DailyLog.log_date <= date_to_obj)

            daily_results = daily_results.group_by(
                Activity.id, Activity.name, Project.id
            ).order_by(Activity.name.asc())

            seen_activities = {item["activity"] for item in activity_list}

            for row in daily_results.all():
                if row.activity_name not in seen_activities:
                    activity_list.append(
                        {
                            "activity": row.activity_name,
                            "hours": 0,
                            "daily_hours": float(round(row.daily_hours or 0, 1)),
                            "users": get_user_dict(
                                project_name,
                                row.activity_name,
                                date_from_obj,
                                date_to_obj,
                            ),
                        }
                    )
                    seen_activities.add(row.activity_name)  # update set

            total_matching = len(activity_list)

        except SQLAlchemyError as e:
            print(f"❌ Database error in get_activity_list: {e}", flush=True)
            activity_list = []
            total_matching = 0

    return activity_list


if __name__ == "__main__":
    get_activity_list("251101-HG", None, None)
