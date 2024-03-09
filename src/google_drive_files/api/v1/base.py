from fastapi import APIRouter

from src.google_drive_files.api.v1.route_files import router

api_router = APIRouter()

api_router.include_router(
    router=router,
    prefix='/v1/google_drive_files',
    tags=['File manager - Sidis Group']
)

