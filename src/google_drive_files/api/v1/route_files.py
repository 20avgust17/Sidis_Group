from fastapi import APIRouter, Depends, File, BackgroundTasks, Request, status

from pydrive.drive import GoogleDrive
from starlette.templating import Jinja2Templates

from src.google_drive_files import schemas
from src.google_drive_files.dependencies import get_google_drive_gauth
from src.google_drive_files.services import GoogleDriveService

router = APIRouter()

# TODO: User interface for all endpoint with jinja2
templates = Jinja2Templates(directory='templates')


@router.get(
    '/index/',
    status_code=status.HTTP_200_OK,
)
async def get_index_page(
        request: Request,
):
    return templates.TemplateResponse(
        name="base.html",
        context={
            'request': request,
        }
    )


@router.get(
    '/files_list/',
    status_code=status.HTTP_200_OK,
)
async def get_list_files(
        request: Request,
        folder_name: str = None,
        drive: GoogleDrive = Depends(get_google_drive_gauth)
):
    return templates.TemplateResponse(
        name="base.html",
        context={
            'request': request,
            'list_files': GoogleDriveService(drive=drive).get_list_files(folder_name=folder_name)
        }
    )


@router.get(
    '/files/{file_name:str}/',
    response_model=schemas.File,
    status_code=status.HTTP_200_OK
)
async def get_file_by_name(
        file_name: str,
        folder_name: str = None,
        drive: GoogleDrive = Depends(get_google_drive_gauth)
):
    return GoogleDriveService(drive=drive).get_file_by_name(
        file_name=file_name,
        folder_name=folder_name
    )


@router.post(
    '/files/',
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def upload_file(
        background_tasks: BackgroundTasks,
        file_name: str,
        file: bytes = File(...),
        folder_name: str = None,
        drive: GoogleDrive = Depends(get_google_drive_gauth),
):
    return GoogleDriveService(drive=drive).create_file(
        background_tasks=background_tasks,
        file_name=file_name,
        file=file,
        folder_name=folder_name
    )


@router.put(
    '/files/',
    response_model=dict,
    status_code=status.HTTP_202_ACCEPTED

)
async def update_file_content(
        background_tasks: BackgroundTasks,
        file_name: str,
        folder_name: str = None,
        file: bytes = File(...),
        drive: GoogleDrive = Depends(get_google_drive_gauth)
):
    return GoogleDriveService(drive=drive).update_file_content(
        background_tasks=background_tasks,
        file_name=file_name,
        folder_name=folder_name,
        new_file=file,
    )


@router.patch(
    '/files/',
    response_model=dict,
    status_code=status.HTTP_202_ACCEPTED

)
async def move_file_into_folders(
        background_tasks: BackgroundTasks,
        file_name: str,
        old_folder_name: str,
        new_folder_name: str,
        drive: GoogleDrive = Depends(get_google_drive_gauth)
):
    return GoogleDriveService(drive=drive).move_file(
        background_tasks=background_tasks,
        file_name=file_name,
        old_folder_name=old_folder_name,
        new_folder_name=new_folder_name,
    )


@router.delete(
    '/files/',
    response_model=dict,
    status_code=status.HTTP_202_ACCEPTED

)
async def delete_file(
        background_tasks: BackgroundTasks,
        file_name: str,
        folder_name: str = None,
        drive: GoogleDrive = Depends(get_google_drive_gauth)
):
    return GoogleDriveService(drive=drive).delete_file_by_name(
        background_tasks=background_tasks,
        file_name=file_name,
        folder_name=folder_name,
    )
