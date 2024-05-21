from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from fastapi import status, HTTPException, Depends
from core.models.user_table import UserOrm
from .schemas_users import UserCreate, UserLogin
from sqlalchemy import select
from sqlalchemy.orm import Session
import hashlib
import bcrypt

async def get_user_by_email(session: AsyncSession, email: str) -> UserOrm:
    query = select(UserOrm).where(UserOrm.user_name == email)
    result = await session.execute(query)
    user = result.scalar_one()
    return user

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

async def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password

async def create_user(session: AsyncSession, user_in: UserCreate) -> UserOrm:
    hashed_password = await hash_password(user_in.password_hash)

    user = UserOrm(
        user_name=user_in.login, email=user_in.email, password_hash=hashed_password
    )

    session.add(user)
    await session.commit()

    return user
