from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from database import get_db
from app.REQUEST.request_models import Request
from app.REQUEST.request_schemas import RequestCreate, RequestUpdate

#Create Request

async def create_request(db: AsyncSession, request: RequestCreate):
    new_request = Request(**request.dict())
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)

#Get all Request starting from 1 and group in 10s
async def get_request(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Request).offset(skip).limit(limit))
    return result.scalars().all()

#Get Request by id
async def get_request_id(db: AsyncSession, request_id):
    result = await db.execute(select(Request).where(Request.id==request_id))
    return result.scalar_one_or_none()

#Update Request
async def update_request(db: AsyncSession, request_id: int, request: RequestUpdate):
    result = await db.execute(select(Request).where(Request.id==request_id))
    requests = result.scalar_one_or_none()
    if not requests:
        return None
    
    for key, value in request.model_dump(exclude_unset=True):
        setattr(requests,key, value)
    await db.commit()
    await db.refresh(requests)
    return requests

#Delete Request
async def delete_request(db: AsyncSession, request_id: int):
    query = delete(Request).where(Request.id==request_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"Request {request_id} deleted successfully"}

