from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode, UnicodeText
from app.db.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(100), nullable=False, index=True)
    description = Column(UnicodeText, nullable=True)  # NVARCHAR(MAX)
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    users = relationship("User", back_populates="team")
    activities = relationship("Activity", back_populates="team")

    def __repr__(self):
        return f"Team(id={self.id}, name={self.name})"
