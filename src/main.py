from fastapi import FastAPI
from pydrive.auth import GoogleAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

from src.google_drive_files.api.v1.base import api_router as google_drive_files_router


def include_router(app: FastAPI):
    app.include_router(google_drive_files_router)


def start_application():

    app = FastAPI(title='Sidis Group Test')
    include_router(app)
    return app


app = start_application()



