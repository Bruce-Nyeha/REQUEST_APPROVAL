from sqlalchemy import Text,Column, String, Numeric,Integer, ForeignKey, DateTime, Enum
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enums import FinanceStatus
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class Finance(Base):
    __tablename__ = "finances"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("requests.id", ondelete="CASCADE"), nullable=True)
    finance_officer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    status = Column(Enum(FinanceStatus), default=FinanceStatus.pending)
    approved_amount = Column(Numeric(10,2), nullable=True)
    remarks = Column(Text, nullable=True)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_onupdate=func.now())


    #User relationship
finance_officer = relationship("User", back_populates="finance_actions")

#Request relationship
request = relationship("Request", back_populates="finance")
