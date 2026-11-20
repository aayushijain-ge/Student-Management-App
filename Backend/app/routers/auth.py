from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.database import get_db
from app.dependencies import get_current_user
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_by_username(db, data.username):
        raise HTTPException(status_code=409, detail="Username already taken")
    return user_service.create_user(db, data)


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return Token(access_token=create_access_token(user.username))


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user