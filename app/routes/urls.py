from fastapi import APIRouter

from .auth_v1 import auth_router
from .test_v1 import test_router


router = APIRouter()


router.include_router(auth_router, prefix="/v1", tags=["auth"])
router.include_router(test_router, prefix="/v1", tags=["test"])