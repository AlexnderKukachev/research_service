"""
This module handles user authentication and registration logic.

Functions:
- get_password_hash: Hashes a plain-text password using bcrypt.
- verify_password: Verifies a plain-text password against a hashed one.
- create_access_token: Generates a JWT access token with an expiration time.
- authenticate_user: Validates user credentials against the database and returns the user if valid.
- get_current_user: Decodes the JWT token and retrieves the corresponding user from the database.

Dependencies:
- FastAPI's OAuth2PasswordBearer is used for token-based authentication.
- JWT is used for encoding and decoding access tokens.
- Async SQLAlchemy is used for database interaction.
"""

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import API_KEY, ALGORITHM
from database import get_db
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # путь для получения токена
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, API_KEY, algorithm=ALGORITHM)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, API_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user