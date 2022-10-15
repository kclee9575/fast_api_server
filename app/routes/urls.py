from fastapi import APIRouter

from .test_v1 import test_router


router = APIRouter()


router.include_router(test_router, prefix="/v1", tags=["dispatch"])
