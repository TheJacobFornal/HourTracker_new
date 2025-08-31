import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.project import Project


def check_insert_user(
    name: str, surname: str
) -> User:  # check if user exist if not insert

    with SessionLocal() as db:
        try:
            name = (name or "").strip()
            surname = (surname or "").strip()

            user = (
                db.query(User)
                .filter(User.name == name, User.surname == surname)
                .first()
            )

            if user:
                return user

            # Not found → create
            user = User(name=name, surname=surname)
            db.add(user)
            db.commit()
            db.refresh(user)
            # print(f"🆕 Inserted new user: {user}")
            return user

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in check_insert_user:", str(e))
            raise


def check_insert_activity(
    name: str,
) -> Activity:  # check if activity exist if not insert

    clean_name = (name or "").strip()
    if not clean_name:
        raise ValueError("Activity name cannot be empty.")

    with SessionLocal() as db:
        try:
            activity = db.query(Activity).filter(Activity.name == clean_name).first()

            if activity:
                return activity

            activity = Activity(name=clean_name, team_id=None, description=None)
            db.add(activity)
            db.commit()
            db.refresh(activity)
            return activity

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in check_insert_activity:", str(e))
            raise


def check_insert_project(name: str) -> Project:  # check if Project exist if not insert
    clean_name = name

    with SessionLocal() as db:
        try:

            project = db.query(Project).filter(Project.name == clean_name).first()

            if project:
                return project

            project = Project(
                name=clean_name,
                client_id=None,
                leader_id=None,
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            return project

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ DB error in check_insert_project:", str(e))
            raise
