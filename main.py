import asyncio
from fastapi import FastAPI
from database import engine, Base
from app.auth.auth_routes import router as auth_router
from app.USER.user_routes import router as user_router
from app.DEPARTMENT.department_routes import router as department_router
from app.REQUEST.request_routes import router as request_router
from app.FINANCE.finance_routes import router as finance_router
from app.REQUESTITEM.request_item_routes import router as request_item_router
from app.PASTOR.pastor_routes import router as pastor_router
from app.APPROVAL.approval_routes import router as approval_router

app = FastAPI(title="Rehoboth Requisition")

#  Async table creation on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # create all tables asynchronously
        await conn.run_sync(Base.metadata.create_all)
    print(" Database tables created successfully!")


#  Include all routers
app.include_router(user_router, prefix="/register-user", tags=["Registration"])
app.include_router(auth_router, prefix="/login", tags=["Login"])
app.include_router(department_router, prefix="/departments", tags=["Departments"])
app.include_router(request_router, prefix="/requests", tags=["Requests"])
app.include_router(finance_router, prefix="/finances", tags=["Finances"])
app.include_router(request_item_router, prefix="/request_items", tags=["RequestItems"])
app.include_router(pastor_router, prefix="/pastors", tags=["Pastors"])
app.include_router(approval_router, prefix="/approvals", tags=["Approvals"])


@app.get("/")
async def root():
    return {
        "message": "Church Request API is running successfully!",
        "status": "ok",
        "docs_url": "/docs",
        "developer": "Mr. Bruce",
        "version": "1.0.0"
    }
