import uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime
from enums import UserRole
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String,  nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.requester, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())   

    #Department relationship 
department = relationship("Department", back_populates="users")

#Request relationship
request = relationship ("Request", back_populates="user")

#Finance relationship
finance_actions= relationship("Finances", back_populates= "financce_officer")

#Pastor relationship
pastor = relationship("Pastor", back_populates="user")