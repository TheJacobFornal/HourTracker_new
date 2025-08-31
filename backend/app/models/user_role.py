from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="UQ_user_roles"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.sysutcdatetime()
    )

    # relations
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user_links")

    def __repr__(self):
        return f"UserRole(id={self.id}, user_id={self.user_id}, role_id={self.role_id})"
