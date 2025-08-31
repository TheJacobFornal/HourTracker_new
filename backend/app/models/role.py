from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode
from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(100), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    user_links = relationship(
        "UserRole", back_populates="role", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Role(id={self.id}, name={self.name})"
