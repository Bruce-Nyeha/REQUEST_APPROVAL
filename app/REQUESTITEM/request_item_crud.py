from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.REQUESTITEM.request_item_models import RequestItem
from app.REQUESTITEM.request_item_schemas import RequestItemCreate, RequestItemUpdate
from app.REQUEST.request_models import Request
from sqlalchemy import func
from decimal import Decimal

#Create RequestItem
async def create_item(item: RequestItemCreate, db: AsyncSession):
    new_item = RequestItem(**item.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

#Get All RequestItem
async def get_request_items(db: AsyncSession, skip: int=0, limit: int=10):
    result = await db.execute(select(RequestItem).offset(skip).limit(limit))
    return result.scalars().all()

#Get RequestItem by id
async def get_request_item_id(item_id: int, db: AsyncSession):
    result = await db.execute(select(RequestItem).where(RequestItem.id==item_id))
    return result.scalar_one_or_none()

#Update RequestItem
async def update_item(item_id: int, item: RequestItemUpdate, db: AsyncSession):
     result = await db.execute(select(RequestItem).where(RequestItem.id==item_id))
     items = result.scalar_one_or_none()
     if not items:
            return None
    
     for key, value in item.model_dump(exclude_unset=True):
            setattr(item,key, value)
     await db.commit
     await db.refresh(items)
     return items

#Delete Request
async def delete_request(db: AsyncSession, item_id: int):
    query = delete(RequestItem).where(RequestItem.id==item_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"Request {item_id} deleted successfully"}

#Calculate the total amount of all items
async def sum_total_amount(request_id: int, db: AsyncSession):
    result = await db.execute(select(func.sum(RequestItem.amount)).where(RequestItem.request_id==request_id))
    total = result.scalar() or Decimal("0.00")
#Upda the request's total_amount
    request = await db.get(Request, request_id)
    if request:
        request.total_amount = total
        await db.commit()
        await db.refresh(request)
    return total
