from sqlalchemy import (
    Column,
    Integer,
    Date,
    DateTime,
    DECIMAL,
    func,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class TimeLog(Base):
    __tablename__ = "time_logs"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "project_id", "activity_id", "log_date", name="UQ_time_logs"
        ),
        CheckConstraint("hours > 0 AND hours <= 24", name="CK_time_logs_hours"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    log_date = Column(Date, nullable=False)
    hours = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    user = relationship("User", back_populates="time_logs")
    project = relationship("Project", back_populates="time_logs")
    activity = relationship("Activity", back_populates="time_logs")

    def __repr__(self):
        return (
            f"TimeLog(id={self.id}, user_id={self.user_id}, project_id={self.project_id}, "
            f"activity_id={self.activity_id}, log_date={self.log_date}, hours={self.hours})"
        )
