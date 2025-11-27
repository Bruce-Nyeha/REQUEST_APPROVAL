from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
from app.APPROVAL.approval_models import ApprovalStatus

class ApprovalBase(BaseModel):
    remarks: Optional[str] = None
    status: Optional[ApprovalStatus] = ApprovalStatus.pending

class ApprovalCreate(ApprovalBase):
    request_id: UUID4
    pastor_id: UUID4


class ApprovalUpdate(ApprovalBase):
    pass 

class ApprovalOut(ApprovalBase):
    id: UUID4
    request_id: UUID4
    pastor_id: UUID4
    approved_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
    