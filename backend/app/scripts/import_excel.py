from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models import (
    User,
    Team,
    Project,
    Activity,
    TimeLog,
)  # others imported automatically via __init__.py


def main():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        try:
            user = User(
                name="Kinga",
                surname="Froianl",
            )
            db.add(user)

            team = Team(
                name="Development Team",
                description="Handles backend and frontend development",
            )
            db.add(team)

            project = Project(name="X!@123412")
            # db.add(project)
            print("✅ Inserted pro :", project)

            activity = Activity(name="Programowaie")
            db.add(activity)

            time_log = TimeLog(
                user_id=1,
                project_id=1,
                activity_id=1,
                log_date="2025-08-22",
                hours=10,
            )
            db.add(time_log)
            print("✅ Inserted log :", time_log)

            db.commit()
            db.refresh(user)

            print("✅ Inserted user:", user)

        except SQLAlchemyError as e:
            db.rollback()
            print("❌ Error inserting user:", str(e))


if __name__ == "__main__":
    main()
