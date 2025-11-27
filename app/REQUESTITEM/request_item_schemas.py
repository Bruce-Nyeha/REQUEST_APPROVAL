from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal

class RequestItemBase(BaseModel):
    description: str
    unit_price: condecimal (max_digits=10, decimal_places=2)
    amount: condecimal(max_digits=10, decimal_places=2)

class RequestItemCreate(RequestItemBase):
    request_id: int

class RequestItemUpdate(BaseModel):
    description: Optional[str] = None
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)]

class RequestItemOut(RequestItemBase):
    id: int
    request_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True