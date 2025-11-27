from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.PASTOR.pastor_crud import (
    create_pastor,
    get_pastors,
    get_pastors_id,
    update_pastor,
    delete_pastor
)
from app.PASTOR.pastor_schemas import PastorCreate, PastorUpdate, PastorOut
from app.auth.dependencies import get_current_user
from app.USER.user_models import User
from database import get_db

router = APIRouter(
    prefix="/pastors",
    tags=["Pastors"]
)

#  Create Pastor
@router.post("/", response_model=PastorOut, status_code=status.HTTP_201_CREATED)
async def create_pastors(
    pastor: PastorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed")

    new_pastor = await create_pastor(pastor=pastor, db=db)
    return new_pastor


#  Get All Pastors
@router.get("/", response_model=list[PastorOut])
async def get_all_pastors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed")

    pastors = await get_pastors(db=db, skip=skip, limit=limit)
    return pastors


#  Get Pastor By ID
@router.get("/{pastor_id}", response_model=PastorOut)
async def get_pastor_by_id(
    pastor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed")

    db_pastor = await get_pastors_id(pastor_id=pastor_id, db=db)
    if not db_pastor:
        raise HTTPException(status_code=404, detail="Pastor not found")
    return db_pastor


#  Update Pastor
@router.put("/{pastor_id}", response_model=PastorOut)
async def pastor_update(
    pastor_id: int,
    update_pastors: PastorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed")

    updated_pastor = await update_pastor(
        pastor_id=pastor_id,
        update_pastors=update_pastors,
        db=db
    )
    if not updated_pastor:
        raise HTTPException(status_code=404, detail="Pastor not found")
    return updated_pastor


#  Delete Pastor
@router.delete("/{pastor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleting_existing_pastor(
    pastor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "pastor":
        raise HTTPException(status_code=403, detail="User not allowed")

    deleted = await delete_pastor(db=db, pastor_id=pastor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pastor not found")
    return None
