# app/models/daily_log.py
from sqlalchemy import (
    Column,
    Integer,
    Date,
    DateTime,
    DECIMAL,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    log_date = Column(Date, nullable=False)
    hours = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.sysutcdatetime(),
    )

    # Relationships
    user = relationship("User", back_populates="daily_logs")
    project = relationship("Project", back_populates="daily_logs")
    activity = relationship("Activity", back_populates="daily_logs")

    def __repr__(self):
        return (
            f"DailyLog(id={self.id}, user_id={self.user_id}, "
            f"project_id={self.project_id}, activity_id={self.activity_id}, "
            f"log_date={self.log_date}, hours={self.hours})"
        )
