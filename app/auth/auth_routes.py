from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from app.auth import auth_crud, hashing, token
from app.USER.user_schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Get user by email OR username
    user = auth_crud.get_user_by_email_or_username(db, form_data.username)

    if not user or not hashing.password_verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    access_token = token.create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role.value}
    )

    # Return token response
    return {"access_token": access_token, "token_type": "bearer"}
