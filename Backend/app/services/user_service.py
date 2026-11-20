from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_by_username(db: Session, username: str):
    return db.scalar(select(User).where(User.username == username))


def create_user(db: Session, data: UserCreate):
    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str):
    user = get_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user