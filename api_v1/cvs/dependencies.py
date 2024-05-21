from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, CVOrm, UserOrm
from . import crud
from ..user.schemas_users import User
from ..user.auth import get_current_user_id


async def cv_by_id(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> any:
    cv = await crud.get_cv(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def cv_photo_by_id(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> any:
    cv = await crud.get_cv_photo(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def cv_contact_info_by_id(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> any:
    cv = await crud.get_contact_info(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def cv_personal_info_by_id(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> any:
    info = await crud.get_personal_info(session=session, cv_id=cv_id)
    if info is not None:
        return info
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def cv_social_links_by_id(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> any:
    cv = await crud.get_social_links(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def get_cv_education(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency)):
    cv = await crud.get_education(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def get_cv_expirience(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency)):
    cv = await crud.get_work_expirience(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def get_cv_languages(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency)):
    cv = await crud.get_languages(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def get_cv_tools(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency)):
    cv = await crud.get_tools(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def get_cv_skills(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency)):
    cv = await crud.get_skills(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def get_cv_courses(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency)):
    cv = await crud.get_courses(session=session, cv_id=cv_id)
    if cv is not None:
        return cv
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"cv {cv_id} not found"
    )


async def delete_cv(
        cv_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
        user=Depends(get_current_user_id)
) -> None:
    await crud.delete_cv(session=session, cv_id=cv_id)


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(db_helper.session_dependency)):
    # Реализуйте логику для получения пользователя по токену
    user = await get_current_user_id(token)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def fetch_user_from_token(token: str, db: AsyncSession = Depends(db_helper.session_dependency)):
    # Реализуйте логику для получения пользователя по токену
    # Это должно быть основано на вашей реализации аутентификации

    user = await db.get(UserOrm, ident=1)  # Временный пример, замените на реальную логику
    return user
