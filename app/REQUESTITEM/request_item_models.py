from sqlalchemy import Integer, Column, Numeric, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from database import Base
from sqlalchemy.sql import func
import datetime

#RequestItem database
class RequestItem(Base):
    __tablename__ = "request_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), index=True)
    description = Column(String(255), nullable=True)
    unit_price = Column(Numeric(10,2 ),  nullable=True)
    amount = Column(Numeric(10, 2), nullable= True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("requests.id"))
    created_at = Column(DateTime(timezone=True), server_default= func.now())
    updated_at = Column(DateTime(timezone=True), server_onupdate= func.now())

    #relationship to Request model
    request = relationship("Request", back_populates="items")
