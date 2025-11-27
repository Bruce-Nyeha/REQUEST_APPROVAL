from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from database import get_db
from app.USER.user_models import User
from fastapi import HTTPException, status, Depends
from app.auth.hashing import password_verify, password_hash
from app.USER.user_schemas import UserCreate, UserLogin

# Create User
async def register_user(db: AsyncSession, user: UserCreate):
    # Check if user already exists by email
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account already exists."
        )
    
    # Hash password
    hashed_pass = password_hash(user.password)
    new_user = User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        password=hashed_pass,
        role=user.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# Get All Users
async def get_user(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = await db.execute(select(User).offset(skip).limit(limit))
    return query.scalars().all()


# Get User by ID
async def get_user_id(user_id: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


# Update User
async def update_user(user_id: str, update_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


# Delete User
async def delete_user(user_id: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    await db.delete(user)
    await db.commit()
    return {"message": f"User {user_id} deleted successfully"}
