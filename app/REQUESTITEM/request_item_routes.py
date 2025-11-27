from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from app.REQUESTITEM.request_item_models import RequestItem
from app.REQUESTITEM.request_item_schemas import RequestItemCreate, RequestItemOut, RequestItemUpdate
from app.REQUESTITEM.request_item_crud import create_item, get_request_items, get_request_item_id, update_item, delete_request

router = APIRouter(
    prefix="/requests_item",
    tags=["RequestsItem"]
)

#Create RequestItem
@router.post("/", response_model=RequestItemOut, status_code=status.HTTP_201_CREATED)
async def create_request_item(item: RequestItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item(db=db, item=item)

#Get All Request
@router.get("/", response_model=RequestItemOut)
async def get_all_request(db: AsyncSession = Depends(get_db)):
    return await get_request_items

#Get Request By id
@router.get("/{item_id}", response_model= RequestItemOut)
async def get_request_by_id(item_id: int, db: AsyncSession = Depends(get_db)):
    db_request = await get_request_by_id(item_id==item_id, db=db)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request Not Found")
    return db_request

#Update Request
@router.put("/{item_id}", response_model= RequestItemUpdate)
async def request_update(item_id: int, item: RequestItemUpdate, db: AsyncSession = Depends(get_db)):
    updated_request = await update_item(item_id=item_id, item=item, db=db)
    if not updated_request:
        raise HTTPException(status_code=404, detail= "Request Not Found")
    return updated_request

# Delete Request
@router.delete("/{item_d}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_existing_request(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_request(item_id=item_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail= "Request Not Found")
    return None