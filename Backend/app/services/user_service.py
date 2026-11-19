from app.core.security import hash_password, verify_password
from app.db.fake_db import users_db
from app.schemas.user import UserCreate


def get_by_username(username: str):
    for user in users_db:
        if user["username"] == username:
            return user
    return None


def create_user(data: UserCreate):
    new_id = max((u["id"] for u in users_db), default=0) + 1
    user = {
        "id": new_id,
        "username": data.username,
        "hashed_password": hash_password(data.password),
    }
    users_db.append(user)
    return user


def authenticate(username: str, password: str):
    user = get_by_username(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user