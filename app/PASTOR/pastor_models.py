from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from uuid import uuid4
from sqlalchemy.sql import func


class Pastor(Base):
    __tablename__ = "pastors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_onupdate=func.now())



    #User relationship
    user = relationship("User", back_populates="pastor")

    #Approval relationship
    approval = relationship("Approval", back_populates="pastor")

    