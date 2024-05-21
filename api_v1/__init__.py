from fastapi import APIRouter

from .cvs.views_cvs import router as cvs_router
from .user.views_users import router as users_router


router = APIRouter()
router.include_router(router=cvs_router, prefix="/cvs")
router.include_router(router=users_router, prefix="/user")

