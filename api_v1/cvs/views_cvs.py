from fastapi import APIRouter, HTTPException, Path, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from . import crud
from .schemas_cvs import CVOrm, CVOrmCreate, CVOrmUpdatePartial
from core.models import db_helper
from .dependencies import cv_by_id, get_current_user, cv_photo_by_id, cv_contact_info_by_id, cv_social_links_by_id, \
    get_cv_tools, get_cv_skills, get_cv_courses, cv_personal_info_by_id
from .dependencies import get_cv_education, get_cv_expirience, get_cv_languages
from fastapi import UploadFile, File
from PIL import Image
import io
import base64
import json

router = APIRouter(tags=["/CVS"])


@router.get("/")
async def get_cvs(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await crud.get_cvs(session=session)
    return {
        "cvs": response
    }


@router.get("/mycvs/")
async def get_my_cvs(
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user=Depends(get_current_user),
):
    response = await crud.get_my_cvs(session=session, user=current_user)
    return {
        "cvs": response
    }


# @router.post("/photo")
# async def upload_photo(photo: UploadFile = File(None),
#     current_user = Depends(get_current_user)):
#     try:
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         photo_url = f"static/{current_user}-{timestamp}.jpg"
#         with open(photo_url, "wb") as uploaded_file:
#             file_content = await photo.read()
#             uploaded_file.write(file_content)
#             uploaded_file.close()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_cv(
        cv_in: CVOrmCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user=Depends(get_current_user),
):
    try:
        if cv_in.photo.url != "":
            image_bytes = base64.b64decode(cv_in.photo.url)
            image = Image.open(io.BytesIO(image_bytes))
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            photo_url = f"static/{current_user}-{timestamp}.png"
            image.save(photo_url)
            cv_in.photo.url = photo_url
        await crud.create_cv(session=session, cv_in=cv_in, user=current_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    response = JSONResponse({
        "Result": "Резюме успешно длобавлено"
    })
    return response


@router.get("/{cv_id}/")
async def get_cv(cv=Depends(cv_by_id), cv_photo=Depends(cv_photo_by_id),
                 cv_contact_info=Depends(cv_contact_info_by_id),
                 cv_social_links=Depends(cv_social_links_by_id),
                 cv_personal_info=Depends(cv_personal_info_by_id),
                 cv_tools=Depends(get_cv_tools),
                 cv_skills=Depends(get_cv_skills),
                 cv_courses=Depends(get_cv_courses),
                 cv_education=Depends(get_cv_education),
                 cv_expirince=Depends(get_cv_expirience),
                 cv_languages=Depends(get_cv_languages)):

    return {
        "cv": cv,
        "photo": cv_photo,
        "personal_info": cv_personal_info,
        "contact_info": cv_contact_info,
        "social_links": cv_social_links,
        "tools": cv_tools,
        "skills": cv_skills,
        "courses": cv_courses,
        "education": cv_education,
        "work_expirience": cv_expirince,
        "languages": cv_languages
    }


@router.put("/{cv_id}/")
async def update_cv(
        cv_id: int,
        cv_update: CVOrmCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user=Depends(get_current_user)
):
    try:
        id = await crud.update_cv(
            session=session,
            cv_id=cv_id,
            cv_in=cv_update,
            user=current_user
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {
        "Result": "ok",
        "CvId": id
    }


@router.patch("/{cv_id}/")
async def update_cv_partial(
        cv_update: CVOrmUpdatePartial,
        cv: CVOrm = Depends(cv_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return {}


@router.delete(
    "/{cv_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_record(
        cv_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    try:
        await crud.delete_cv(cv_id=cv_id, user_id=user, session=session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    response = JSONResponse({
        "Result": "Резюме удалено"
    })
