import asyncio
import logging
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES
import auth
from crud import (
    get_samples, get_sample,
    create_sample, update_sample,
    delete_sample
)
from database import get_db, engine, Base
from schemas import Sample, SampleCreate, SampleUpdate
from models import User
from schemas import UserCreate, UserOut, Token

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create database tables
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(
    title="Research Sample Service",
    version="1.0.0",
    description="API для управления образцами исследований",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/samples', response_model=List[Sample])
async def read_samples(sample_type: str = None, status: str = None, current_user: User = Depends(auth.get_current_user)):
    logger.info("Fetching samples; type=%s status=%s", sample_type, status)
    return await get_samples(sample_type, status)

@app.get('/samples/{sample_id}', response_model=Sample)
async def read_sample(sample_id: str, current_user: User = Depends(auth.get_current_user)):
    logger.info("Fetching sample %s", sample_id)
    sample = await get_sample(sample_id)
    if not sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return sample

@app.post('/samples', response_model=Sample, status_code=status.HTTP_201_CREATED)
async def create_new_sample(sample: SampleCreate, current_user: User = Depends(auth.get_current_user)):
    logger.info("Creating new sample %s", sample.sample_id)
    return await create_sample(sample)

@app.put('/samples/{sample_id}', response_model=Sample)
async def update_existing_sample(sample_id: str, sample: SampleUpdate, current_user: User = Depends(auth.get_current_user)):
    logger.info("Updating sample %s with %s", sample_id, sample.dict())
    updated = await update_sample(sample_id, sample)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return updated

@app.delete('/samples/{sample_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_sample(sample_id: str, current_user: User = Depends(auth.get_current_user)):
    logger.info("Deleting sample %s", sample_id)
    success = await delete_sample(sample_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if db_user:
        logger.warning(f"Попытка регистрации с уже существующим именем пользователя: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = auth.get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"Пользователь зарегистрирован: {new_user.username}")
    return new_user

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Неудачная попытка входа: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    logger.info(f"Пользователь вошёл в систему: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
