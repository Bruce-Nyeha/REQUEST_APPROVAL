from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from app.PASTOR.pastor_models import Pastor
from app.PASTOR.pastor_schemas import PastorBase, PastorCreate, PastorUpdate, PastorOut


#Create Pastor
async def create_pastor(pastor: PastorCreate, db: AsyncSession):
    new_pastor = Pastor(**pastor.dict())
    await db.add(new_pastor)
    await db.commit()
    await db.refresh(new_pastor)


#Get All Pastor in Paginated Form
async def get_pastors(db: AsyncSession, skip: int= 0, limit: int=10):
    query = await db.execute(select(Pastor).offset(skip).limit(limit))
    return query.scalars().all()

#Get All Pastor by id
async def get_pastors_id(pastor_id: int, db: AsyncSession):
    pastor = await db.execute(select(Pastor).where(Pastor.id==pastor_id))
    return pastor.scalar_one_or_none()

#Update Pastor
async def update_pastor(pastor_id: int, update_pastors: PastorUpdate, db: AsyncSession):
    result = await db.execute(select(Pastor).where(Pastor.id==pastor_id))
    pastor = result.scalar_one_or_none()
    if not pastor:
        return None
    
    for key, value in update_pastors.model_dump(exclude_unset=True):
        setattr(pastor,key, value)
    await db.commit()
    await db.refresh(pastor)
#Delete Pastor
async def delete_pastor(db: AsyncSession, pastor_id: int):
    query = delete(Pastor).where(Pastor.id==pastor_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"Pastor {pastor_id} deleted successfully"}
