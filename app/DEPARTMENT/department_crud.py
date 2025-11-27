from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.DEPARTMENT.department_models import Department
from app.DEPARTMENT.department_schemas import DepartmentCreate, DepartmentUpdate
from database import get_db 


#Create Department
async def create_department(db: AsyncSession, department: DepartmentCreate):
    new_department = Department(**department.dict())
    db.add(new_department)
    await db.commit()
    await db.refresh(new_department)
    return new_department


#Get All Departments
async def get_departments(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Department).offset(skip).limit(limit))
    return result.scalars().all()


#Get Departments by id
async def get_department_by_id(db: AsyncSession, department_id: int):
    result = await db.execute(select(Department).where(Department.id == department_id))
    return result.scalar_one_or_none()


#Update Department
async def update_department(db: AsyncSession, department_id: int, department: DepartmentUpdate):
        result = await db.execute(select(Department).where(Department.id==department_id))
        departments = result.scalar_one_or_none()
        if not departments:
            return None
    
        for key, value in departments.model_dump(exclude_unset=True):
            setattr(departments,key, value)
        await db.commit()
        await db.refresh(departments)
        return departments

#Delete Department
async def delete_department(db: AsyncSession, department_id: int):
    query = delete(Department).where(Department.id == department_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"Department {department_id} deleted successfully"}
