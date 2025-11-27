from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.DEPARTMENT.department_schemas import DepartmentCreate, DepartmentUpdate, DepartmentOut
from app.DEPARTMENT.department_crud import get_department_by_id, get_departments, create_department, delete_department, update_department

from database import get_db

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

# Create Department
@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
async def create_new_department(
    department: DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_department(db=db, department=department)


# Get All Departments
@router.get("/", response_model=List[DepartmentOut])
async def read_departments(db: AsyncSession = Depends(get_db)):
    return await get_departments(db=db)


# Get Department by ID
@router.get("/{department_id}", response_model=DepartmentOut)
async def read_department(department_id: int, db: AsyncSession = Depends(get_db)):
    db_department = await get_department_by_id(db=db, department_id=department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department Not Found")
    return db_department


# Update Department
@router.put("/{department_id}", response_model=DepartmentOut)
async def update_existing_department(
    department_id: int,
    department: DepartmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_department = await update_department(db, department_id, department)
    if not updated_department:
        raise HTTPException(status_code=404, detail="Department Not Found")
    return updated_department


# Delete Department
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_department(department_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_department(db, department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department Not Found")
    return None
