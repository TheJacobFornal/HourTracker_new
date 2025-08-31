from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode
from app.db.base import Base  # 👈 import from base_class, not base.py


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(150), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    projects = relationship("Project", back_populates="client")

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name})"
