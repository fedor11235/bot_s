from fastapi import APIRouter
from src.apis.common import router as commonRouter
apis = APIRouter()
apis.include_router(commonRouter)
__all__ = ["apis"]