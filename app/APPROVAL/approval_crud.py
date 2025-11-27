from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.APPROVAL.approval_models import Approval
from app.APPROVAL.approval_schemas import ApprovalCreate, ApprovalUpdate
from datetime import datetime

# Create approval (by Pastor after Finance review)
async def create_approval(data: ApprovalCreate, db: AsyncSession):
    new_approval = Approval(**data.model_dump())
    db.add(new_approval)
    await db.commit()
    await db.refresh(new_approval)
    return new_approval


#  Get all approvals (paginated)
async def get_all_approvals(skip: int, limit: int, db: AsyncSession):
    result = await db.execute(select(Approval).offset(skip).limit(limit))
    return result.scalars().all()


#  Get approval by ID
async def get_approval_by_id(approval_id: int, db: AsyncSession):
    result = await db.execute(select(Approval).where(Approval.id == approval_id))
    return result.scalar_one_or_none()


# update approval (approve or reject)
async def update_approval(approval_id: int, data: ApprovalUpdate, db: AsyncSession):
    result = await db.execute(select(Approval).where(Approval.id == approval_id))
    approval = result.scalar_one_or_none()

    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(approval, key, value)

    approval.updated_at = datetime.utcnow()

    db.add(approval)
    await db.commit()
    await db.refresh(approval)
    return approval


#  Delete approval (admin or pastor only)
async def delete_approval(approval_id: int, db: AsyncSession):
    result = await db.execute(select(Approval).where(Approval.id == approval_id))
    approval = result.scalar_one_or_none()

    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")

    await db.delete(approval)
    await db.commit()
    return True
