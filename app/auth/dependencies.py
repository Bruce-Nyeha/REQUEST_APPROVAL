from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.token import verify_access_token
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
"""Now we create our function to get dependencies or get current user for protecting our routes."""

async def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        details = "Invalid or expired credentials",
        headers={"WWW-Authenticate": "Bearer"}
    ) 
    return await verify_access_token(token, credentials_exception)
