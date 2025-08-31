import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog


def get_user(name, surname):
    with SessionLocal() as db:
        user = db.query(User).filter(User.name == name, User.surname == surname).first()

        if user:
            return user
        else:
            return None


def get_Activity(name):
    with SessionLocal() as db:
        activity = db.query(Activity).filter(Activity.name == name).first()

        if activity:
            return activity
        else:
            return None


def get_Project(name):
    with SessionLocal() as db:
        project = db.query(Project).filter(Project.name == name).first()

        if project:
            return project
        else:
            return None


def check_insert_timeLog(
    name: str,
    surname: str,
    project_name: str,
    activity_name: str,
    log_date: datetime.date,
    hours: float,
) -> TimeLog:
    """
    Insert a time log record, automatically creating missing users, projects, or activities.
    Returns the TimeLog row.
    """

    with SessionLocal() as db:
        try:
            user = get_user(name, surname)
            project = get_Project(project_name)
            activity = get_Activity(activity_name)

            if not all([name, surname, str(project_name), activity.name]):
                raise ValueError(
                    "User name, project name, and activity name cannot be empty."
                )

            # Check for existing time log
            existing_log = (
                db.query(TimeLog)
                .filter(
                    TimeLog.user_id == user.id,
                    TimeLog.project_id == project.id,
                    TimeLog.activity_id == activity.id,
                    TimeLog.log_date == log_date,
                )
                .first()
            )

            if existing_log:
                return existing_log

            # Create new time log
            time_log = TimeLog(
                user_id=user.id,
                project_id=project.id,
                activity_id=activity.id,
                log_date=log_date,
                hours=hours,
            )
            db.add(time_log)
            db.commit()
            db.refresh(time_log)
            return time_log

        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Database error in check_insert_timeLog: {str(e)}")
            raise
