from fastapi import APIRouter, HTTPException, Depends, status
from app.USER import user_crud, user_models, user_schemas
from app.USER.user_schemas import UserResponse, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.USER.user_crud import register_user, get_user, get_user_id, update_user, delete_user
from database import get_db
from typing import List
router = APIRouter(prefix="/register-user", tags=["Registration"])

#Create User
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: AsyncSession = Depends(get_db), user: UserCreate=Depends()):
    return await register_user(db=db, user=user)

#Get All Users
@router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession=Depends(get_db)):
    return await get_user


#Get User by id
@router.get("{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession=Depends(get_db)):
    return await get_user_id(user_id=user_id, db=db)

#Update User
@router.put("/{user_id}", response_model=UserResponse)
async def user_update(user_id: int, db: AsyncSession=Depends(get_db), update_data: UserResponse=Depends()):
    updated_user = await update_user(db=db, user_id=user_id, update_data=update_data)
    if not update_data:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


#Delete User
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: int, db: AsyncSession=Depends(get_db)):
    deleted = await delete_user(user_id=user_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None