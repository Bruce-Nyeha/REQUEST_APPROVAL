from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.FINANCE.finance_models import Finance, FinanceStatus
from app.REQUEST.request_models import Request
from datetime import datetime
from app.FINANCE.finance_schemas import FinanceCreate, FinanceUpdate
import decimal



#Create Finance function
async def create_finance(finance: FinanceCreate, db: AsyncSession):
    new_finance = Finance(**finance.dict())
    db. add(new_finance)
    await db.commit()
    await db.refresh(new_finance)

#Get All Finances
async def get_finance(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Finance).offset(skip).limit(limit))
    return result.scalars().all()

#Get All Finances by id
async def get_finance_id(finance_id: int, db: AsyncSession):
    finance = await db.execute(select(Finance).where(Finance.id==finance_id))
    return finance.scalar_one_or_none()

#Update Finance
async def update_finance(finance_id: int, update_finance: FinanceUpdate, db: AsyncSession):
    result = await db.execute(select(Finance).where(Finance.id==finance_id))
    finance = result.scalar_one_or_none()
    if not finance:
        return None
    
    for key, value in update_finance.model_dump(exclude_unset=True):
        setattr(finance,key, value)
    await db.commit()
    await db.refresh(finance)
#Delete Finance
async def delete_finance(db: AsyncSession, finance_id: int):
    query = delete(Finance).where(Finance.id==finance_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"Finance {finance_id} deleted successfully"}


"""The main backend logic for the Finance Department to review request."""

async def review_finance_request(finance_id: int, approved_amount: decimal, remarks: str, db: AsyncSession):
    result =  await db.execute(select(Finance).where(Finance.id==finance_id))
    finance = result.scalar_one_or_none()
    
    if not finance:
        return None
    
    finance.approved_amount = approved_amount
    finance.remarks = remarks 
    finance.status = FinanceStatus.approved
    finance.updated_at = datetime.utcnow()

    result = await db.execute(select(Request).where(Request.id==finance.request_id))
    request = result.scalar_one_or_none()
    if request:
        request.status = "awaiting_pastors_approval"

    await db.commit()
    await db.refresh(finance)
    return finance


