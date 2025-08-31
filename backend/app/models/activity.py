from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        # unique per team when team_id is not null
        Index(
            "UX_activities_team_name", "team_id", "name", unique=True, mssql_where=None
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(100), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    description = Column(Unicode(200), nullable=True)
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    team = relationship("Team", back_populates="activities")
    time_logs = relationship("TimeLog", back_populates="activity")

    def __repr__(self):
        return f"Activity(id={self.id}, name={self.name}, team_id={self.team_id})"
