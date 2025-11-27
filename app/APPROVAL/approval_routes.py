from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.APPROVAL.approval_crud import (
    create_approval,
    get_all_approvals,
    get_approval_by_id,
    update_approval,
    delete_approval,
)
from app.APPROVAL.approval_schemas import ApprovalCreate, ApprovalUpdate, ApprovalOut
from app.auth.dependencies import get_current_user
from app.USER.user_models import User
from database import get_db


router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


# 🟢 Create Approval
@router.post("/", response_model=ApprovalOut, status_code=status.HTTP_201_CREATED)
async def create_approvals(
    approval: ApprovalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed to create approvals")

    new_approval = await create_approval(approval=approval, db=db)
    return new_approval


#  Get All Approvals
@router.get("/", response_model=list[ApprovalOut])
async def get_all_approval_list(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["pastor", "finance"]:
        raise HTTPException(status_code=403, detail="User not allowed to view approvals")

    approvals = await get_all_approvals(db=db, skip=skip, limit=limit)
    return approvals


#  Get Approval by ID
@router.get("/{approval_id}", response_model=ApprovalOut)
async def get_approval_by_id(
    approval_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["pastor", "finance"]:
        raise HTTPException(status_code=403, detail="User not allowed to view this approval")

    approval = await get_approval_by_id(approval_id=approval_id, db=db)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")

    return approval


#  Update Approval (Approve or Reject)
@router.put("/{approval_id}", response_model=ApprovalOut)
async def update_approval_route(
    approval_id: int,
    update_data: ApprovalUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed to update approvals")

    updated = await update_approval(approval_id=approval_id, update_approvals=update_data, db=db)
    if not updated:
        raise HTTPException(status_code=404, detail="Approval not found")

    return updated


#  Delete Approval
@router.delete("/{approval_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approval_route(
    approval_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed to delete approvals")

    deleted = await delete_approval(approval_id=approval_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Approval not found")

    return None
