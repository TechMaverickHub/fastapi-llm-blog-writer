from sqlalchemy import Column, Integer, DateTime, Boolean, func, String, Text, ForeignKey
from app.database import Base


class Blog(Base):
    __tablename__ = "blogs"


    # Foreign Key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Fields
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    # Additional Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
