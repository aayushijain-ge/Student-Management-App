import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.services import user_service

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = user_service.get_by_username(db, payload.get("sub", ""))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user