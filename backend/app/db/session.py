# app/db/sess_remote.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import urllib.parse as _u

SERVER = r"localhost"
DATABASE = "HourTrackerDB"
USER = "sa"
PWD = "YourStrong!Passw0rd"  # escape backslash for Python

_odbc = _u.quote_plus(
    f"DRIVER=ODBC Driver 17 for SQL Server;"
    f"SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PWD};"
    "Encrypt=no;"
)
engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={_odbc}", echo=False, future=True
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# quick self-test
if __name__ == "__main__":
    with engine.connect() as c:
        print("✅ SQLAlchemy connected")
        print(c.execute(text("SELECT DB_NAME(), SUSER_SNAME()")).all())
