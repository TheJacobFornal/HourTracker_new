from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        # filtered unique index: email is unique only when NOT NULL
        Index(
            "UX_users_email_notnull",
            "email",
            unique=True,
            mssql_where=text("email IS NOT NULL"),
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(100), nullable=False)
    surname = Column(Unicode(100), nullable=False)
    team_id = Column(
        Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True
    )
    email = Column(Unicode(255), nullable=True)
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    team = relationship("Team", back_populates="users")
    roles = relationship(
        "UserRole", back_populates="user", cascade="all, delete-orphan"
    )
    time_logs = relationship("TimeLog", back_populates="user")

    # projects where this user is the leader
    projects_led = relationship(
        "Project", back_populates="leader", foreign_keys="Project.leader_id"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, surname={self.surname}, email={self.email})"
