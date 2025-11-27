from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.FINANCE.finance_models import Finance
from app.FINANCE.finance_crud import create_finance, get_finance, get_finance_id,update_finance, delete_finance, review_finance_request
from app.FINANCE.finance_schemas import FinanceCreate, FinanceUpdate, FinanceResponse, FinanceReviewSchema
from database import get_db
from app.auth.dependencies import get_current_user
from app.USER.user_models import User

router = APIRouter(
    prefix= "/finances",
    tags= ["Finances"]
)

#Create Finance
@router.post("/", response_model=FinanceResponse, status_code=status.HTTP_201_CREATED)
async def create_finance(finance: FinanceCreate, db: AsyncSession = Depends(get_db)):
    return await create_finance(db=db, finance=finance)

#Get All Finance
@router.get("/", response_model=FinanceResponse)
async def get_all_fiance(db: AsyncSession = Depends(get_db)):
    return await get_finance


#Get Finance By id
@router.get("/{finance_id}", response_model= FinanceResponse)
async def get_finance_by_id(finance_id: int, db: AsyncSession = Depends(get_db)):
    db_finance = await get_finance_id(finance_id=finance_id, db=db)
    if not db_finance:
        raise HTTPException(status_code=404, detail="Finance Not Found")
    return db_finance

#Update Finance
@router.put("/{finance_id}", response_model= FinanceUpdate)
async def finance_update(finance_id: int, update_finance: FinanceUpdate, db: AsyncSession = Depends(get_db)):
    updated_finance = await update_finance(finance_id=finance_id, update_finance=update_finance, db=db)
    if not updated_finance:
        raise HTTPException(status_code=404, detail= "Finance Not Found")
    return updated_finance

# Delete Finance
@router.delete("/{finance_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_existing_finance(finance_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_finance(finance_id=finance_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail= "Finance Not Found")
    return None


@router.put("/{finance_id}/review",  response_model=FinanceResponse)
async def review_finance_request(
    finance_id: int,
    data: FinanceReviewSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "finance_officer":
        raise HTTPException(status_code=403, detail="Not authorized to review")
    
    finance = await review_finance_request(
        finance_id=finance_id,
        approved_amount=data.approved_amount,
        remarks = data.remarks,
        db=db
    )
    if not finance:
        raise HTTPException(status_code=404, detail="Finance record not found")