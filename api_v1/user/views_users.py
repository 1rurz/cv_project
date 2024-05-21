from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from core.models import db_helper
from .schemas_users import UserCreate, UserLogin
from . import cr_user
from pydantic import BaseModel, EmailStr
from .auth import create_access_token, get_current_user_id
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound

router = APIRouter(tags=["/USERS"])


class UserResponse(BaseModel):
    user_name: str
    email: str


@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(db_helper.session_dependency)):
    try:
        user = await cr_user.get_user_by_email(session, form_data.username)
        if not await cr_user.verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token = create_access_token({"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        if user_in.login == "" or user_in.password_hash == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Empty credentials",
            )
        user = await cr_user.create_user(session=session, user_in=user_in)
        return user
    except Exception as e:
        if str(e) == "422: Empty credentials":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Empty credentials",
            )
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
                )

