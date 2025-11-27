from pydantic import BaseModel,condecimal, UUID4
from decimal import Decimal
from typing import Optional
from datetime import datetime
from enums import FinanceStatus

class FinanceBase(BaseModel):
    status: Optional[FinanceStatus] = FinanceStatus.pending
    approved_amount: Optional[(condecimal(max_digits=10, decimal_places=2))] = None
    remarks: Optional[str]
    payment_date: Optional[datetime] = None

class FinanceCreate(FinanceBase):
    request_id: int
    finance_officer_id: Optional[int] = None

class FinanceUpdate(FinanceBase):
    pass

class FinanceResponse(FinanceBase):
    id: UUID4
    request_id: int
    finance_officer_id: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class FinanceReviewSchema(BaseModel):
    approved_amount: Decimal
    remarks: Optional[str]

    class Config:
        from_attributes = True

