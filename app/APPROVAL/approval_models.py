from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from enums import ApprovalStatus
from database import Base


class Approval(Base):
    __tablename__ = "approvals"
    id = Column(UUID(as_uuid=True), primary_key =True, default= uuid4(),index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    pastor_id = Column(UUID(as_uuid=True), ForeignKey("pastors.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.pending)
    remarks = Column(Text, nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True, server_onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #Request relationship
    request = relationship("Request", back_populates="approval")

    #Pastor relationship
    pastor = relationship("Pastor", back_populates="approvals")