import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project
from app.models.time_log import TimeLog
from app.models.time_logs_daily import DailyLog
from sqlalchemy import extract
from sqlalchemy.exc import SQLAlchemyError


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


def check_insert_daily_timelogs(
    name: str,
    surname: str,
    project_name: str,
    activity_name: str,
    log_date: datetime.date,
    hours: float,
) -> DailyLog:
    """
    Insert a daily log record, automatically creating missing users, projects, or activities.
    Returns the DailyLog row.
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

            # Check for existing daily log
            existing_log = (
                db.query(DailyLog)
                .filter(
                    DailyLog.user_id == user.id,
                    DailyLog.project_id == project.id,
                    DailyLog.activity_id == activity.id,
                    DailyLog.log_date == log_date,
                )
                .first()
            )

            if existing_log:
                # print("daily log already exists", existing_log, flush=True)
                return existing_log

            # Create new daily log
            TimeLogDaily_record = DailyLog(
                user_id=user.id,
                project_id=project.id,
                activity_id=activity.id,
                log_date=log_date,
                hours=hours,
            )

            # print("adding daily log", TimeLogDaily_record, flush=True)
            db.add(TimeLogDaily_record)
            db.commit()
            db.refresh(TimeLogDaily_record)
            return TimeLogDaily_record

        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Database error in check_insert_daily_timeLog: {str(e)}")
            raise


def test_daily():

    with SessionLocal() as db:
        try:
            TimeLogDaily_record = DailyLog(
                user_id="2",
                project_id="2",
                activity_id="1",
                log_date="2024-06-01",
                hours="11",
            )

            db.add(TimeLogDaily_record)
            db.commit()
            db.refresh(TimeLogDaily_record)

        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Database error in check_insert_daily_timeLog: {str(e)}")
            raise


def delete_temp_monthly_data(year: int, month: int) -> None:
    """
    Deletes all DailyLog records for the given year and month.
    Useful for clearing temporary or imported data before reimporting.
    """
    with SessionLocal() as db:
        try:
            deleted_count = (
                db.query(DailyLog)
                .filter(
                    extract("year", DailyLog.log_date) == year,
                    extract("month", DailyLog.log_date) == month,
                )
                .delete(synchronize_session=False)
            )
            db.commit()
            print(
                f"✅ Usunięto {deleted_count} recordów z tabeli tymczasowej z {year}-{month:02d}"
            )
        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Database error in delete_temp_monthly_data: {str(e)}")
            raise


if __name__ == "__main__":
    check_insert_daily_timelogs()
