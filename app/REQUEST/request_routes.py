from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.REQUEST.request_models import Request
from app.REQUEST.request_crud import create_request, get_request, get_request_id, update_request, delete_request
from app.REQUEST.request_schemas import RequestCreate, RequestUpdate, RequestOut
from database import get_db

router = APIRouter(
    prefix= "/requests",
    tags= ["Requests"]
)

#Create Request
@router.post("/", response_model=RequestOut, status_code=status.HTTP_201_CREATED)
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    return await create_request(db=db, request=request)

#Get All Request
@router.get("/", response_model=RequestOut)
async def get_all_request(db: AsyncSession = Depends(get_db)):
    return await get_request


#Get Request By id
@router.get("/{request_id}", response_model= RequestOut)
async def get_request_by_id(request_id: int, db: AsyncSession = Depends(get_db)):
    db_request = await get_request_id(request_id=request_id, db=db)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request Not Found")
    return db_request

#Update Request
@router.put("/{request_id}", response_model= RequestUpdate)
async def request_update(request_id: int, request: RequestUpdate, db: AsyncSession = Depends(get_db)):
    updated_request = await update_request(request_id=request_id, request=request, db=db)
    if not updated_request:
        raise HTTPException(status_code=404, detail= "Request Not Found")
    return updated_request

# Delete Request
@router.delete("/{request_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_existing_request(request_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_request(request_id=request_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail= "Request Not Found")
    return None