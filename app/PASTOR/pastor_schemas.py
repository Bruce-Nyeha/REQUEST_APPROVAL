from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class PastorBase(BaseModel):
    title: str
    
class PastorCreate(PastorBase):
    user_id: UUID4

class PastorUpdate(PastorBase):
    pass

class PastorOut(PastorBase):
    id: UUID4
    user_id: Optional[UUID4]= None
    created_at: datetime

    class Config:
        from_attributes = True