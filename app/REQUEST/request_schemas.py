from pydantic import BaseModel, condecimal
from typing import Optional, List
from datetime import datetime

class RequestBase(BaseModel):
    description: Optional[str] = None
    title: str

class RequestCreate(RequestBase):
    pass

class RequestUpdate(RequestBase):
    pass

class RequestOut(RequestBase):
    id: int
    user_id: int
    department_id: int
    status: str
    total_amount: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime
    updated_at: datetime
    

    class Config:
        from_attributes = True

        