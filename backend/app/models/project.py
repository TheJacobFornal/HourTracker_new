from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func,
    ForeignKey,
    CheckConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import UnicodeText, Unicode
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint(
            "status IN (N'Finished', N'In process')", name="CK_projects_status"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(UnicodeText, nullable=False, unique=True)
    client_id = Column(
        Integer, ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # allow None
    status = Column(Unicode(20), nullable=False, server_default="In process")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text(
            "(SYSUTCDATETIME() AT TIME ZONE 'UTC' AT TIME ZONE 'GMT Standard Time')"
        ),
    )

    # Relations
    client = relationship("Client", back_populates="projects")
    leader = relationship(
        "User", back_populates="projects_led", foreign_keys=[leader_id]
    )
    time_logs = relationship("TimeLog", back_populates="project")

    def __repr__(self):
        return (
            f"Project(id={self.id}, name='{self.name}', leader_id={self.leader_id}, "
            f"status='{self.status}', created_at={self.created_at})"
        )
