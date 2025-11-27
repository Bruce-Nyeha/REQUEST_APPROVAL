from sqlalchemy import Integer, String, DateTime, Column, Enum, Text, ForeignKey, Numeric
from uuid import uuid4
from datetime import datetime
from enums import RequestStatus
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

#Request Model from User
class Request(Base):
    __tablename__ = "requests"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4(), index=True)
    description = Column(Text, nullable=True)
    title = Column(String, nullable=True)   
    user_id =  Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending)
    total_amount = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    #User relationship
user = relationship("User", back_populates="request")

#Department relationship
department = relationship("Department", back_populates="request")

#RequestItem relationship
items = relationship("RequestItem", back_populates="request")

#Finance relationship
finance = relationship("Finances", back_populates="request")



#Approval relationship
approvals = relationship("Approval", back_populates="request")
