import logging
from io import BytesIO

from fastapi import BackgroundTasks, status
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile

from src import utils
from src.google_drive_files.exceptions import (
    InvalidUploadFile, InvalidExecutionRequest, InvalidUpdateFile, InvalidMoveFile, InvalidDeleteFile)


class GoogleDriveService:

    def __init__(self, drive: GoogleDrive):
        self.drive = drive

    def get_list_files(self, folder_name: str) -> list[dict]:

        if folder_name:
            folder_id = self.get_folder_id_by_name(drive=self.drive, folder_name=folder_name)
            file_query = f"'{folder_id}' in parents and trashed=false"
        else:
            file_query = "mimeType != 'application/vnd.google-apps.folder' and trashed=false"

        file_list = self.drive.ListFile({'q': file_query}).GetList()

        # validating the existence of objects and checking for duplicates
        self._validate_exist(file_list, folder_name)

        return [{'id': file['id'], 'title': file['title']} for file in file_list]

    def get_file_by_name(self, file_name: str, folder_name: str = None) -> dict:
        # Forming a request and validating the result
        file = self._execute_query_and_apply_validators(file_name, folder_name)

        return {'id': file['id'], 'title': file['title']}

    def get_folder_id_by_name(self, drive: GoogleDrive, folder_name: str) -> str:
        try:
            folder_list = drive.ListFile({
                'q': f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"}
            ).GetList()

        except InvalidExecutionRequest:
            utils.raise_exception_if_true(
                item=True,
                on_error_message=f"Something went wrong when we getting folder id. Detail: {InvalidExecutionRequest}.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # validating the existence of objects and checking for duplicates
        self._validate_exist(folder_list, folder_name)
        self._validate_duplicate_by_name(folder_list)

        return folder_list[0]['id']

    def create_file(
            self,
            background_tasks: BackgroundTasks,
            file_name: str,
            file: bytes,
            folder_name: str = None
    ) -> dict:

        folder_id = self.get_folder_id_by_name(self.drive, folder_name) if folder_name else None

        background_tasks.add_task(self._upload_file_in_drive, file_name, file, folder_id)

        return {"Detail": 'Your file has been added to the queue to be added to Google Drive'}

    def update_file_content(
            self,
            background_tasks: BackgroundTasks,
            file_name: str,
            new_file: bytes,
            folder_name: str = None
    ) -> dict:
        # Forming a request and validating the result
        file = self._execute_query_and_apply_validators(file_name, folder_name)

        background_tasks.add_task(self._update_file_in_drive, file_name, file, new_file)

        return {"Detail": 'Your file has been added to the queue to be updated in Google Drive'}

    def move_file(
            self,
            background_tasks: BackgroundTasks,
            file_name: str,
            old_folder_name: str,
            new_folder_name
    ) -> dict:
        # Forming a request and validating the result
        file = self._execute_query_and_apply_validators(file_name, old_folder_name)

        background_tasks.add_task(self._move_file_in_drive, file_name, file, new_folder_name)
        logging.info(f'A file named: {file_name} will be moved from {old_folder_name} to {new_folder_name}')

        return {"Detail": f'Your file named: {file_name} has been added to the queue to be move to other folder'}

    def delete_file_by_name(self, background_tasks: BackgroundTasks, file_name: str, folder_name: str = None) -> dict:
        # forming a request and validating the result
        file = self._execute_query_and_apply_validators(file_name, folder_name)

        background_tasks.add_task(self._delete_file_in_drive, file_name, file)
        logging.info(f'A file named: {file_name} will be deleted.')

        return {"Detail": f'Your file named: {file_name} has been added to the queue to be delete.'}

    def _move_file_in_drive(self, file_name: str, file: GoogleDriveFile, new_folder_name: str) -> None:
        try:
            # Folder updates
            file['parents'] = [{'id': self.get_folder_id_by_name(drive=self.drive, folder_name=new_folder_name)}]
            file.Upload()
        except InvalidMoveFile:
            logging.info(f'An error occurred while moving a file named {file_name} to Other folder.')

        logging.info(f'A file named: {file_name}, Successfully move in Other folder.')

    def _upload_file_in_drive(self, file_name: str, file: bytes, folder_id: str = None) -> None:

        file_metadata = {'title': file_name}
        if folder_id:
            file_metadata['parents'] = [{'kind': 'drive#fileLink', 'id': folder_id}]

        try:
            file_drive = self.drive.CreateFile(metadata=file_metadata)
            file_drive.content = BytesIO(file)
            file_drive.Upload()
        except InvalidUploadFile:
            logging.info(f'An error occurred while uploading a file named {file_name}.')

        logging.info(f'A file named: {file_name}, Successfully saved.')

    @staticmethod
    def _update_file_in_drive(file_name: str, file: GoogleDriveFile, new_file: bytes) -> None:
        try:
            file.content = BytesIO(new_file)
            file.Upload()
        except InvalidUpdateFile:
            logging.info(f'An error occurred while updating a file named {file_name}.')

        logging.info(f'A file named: {file_name}, Successfully updated.')

    @staticmethod
    def _delete_file_in_drive(file_name: str, file: GoogleDriveFile) -> None:
        try:
            file.Delete()
        except InvalidDeleteFile:
            logging.info(f'An error occurred while deleting a file named {file_name}.')

        logging.info(f'A file named: {file_name}, Successfully deleted.')

    def _execute_query_and_apply_validators(self, file_name: str, folder_name: str) -> GoogleDriveFile:
        try:
            if folder_name:
                folder_id = self.get_folder_id_by_name(drive=self.drive, folder_name=folder_name)
                query = f"title='{file_name}' and '{folder_id}' in parents and trashed=false"
            else:
                query = f"title='{file_name}' and trashed=false"
            file_list = self.drive.ListFile({'q': query}).GetList()
        except InvalidExecutionRequest:
            utils.raise_exception_if_true(
                item=True,
                on_error_message=f"Something went wrong when we getting info from Google Drive. "
                                 f"Detail: {InvalidExecutionRequest}.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # validating the existence of objects and checking for duplicates
        self._validate_exist(file_list, folder_name)
        self._validate_duplicate_by_name(file_list)

        return file_list[0]

    @staticmethod
    def _validate_duplicate_by_name(folder_or_file: list) -> None:
        utils.raise_exception_if_true(
            item=len(folder_or_file) > 1,
            on_error_message=f"Your folders or files are duplicated by name. Please remove duplicate items",
            status_code=status.HTTP_409_CONFLICT
        )

    @staticmethod
    def _validate_exist(folder_or_file_list: list, folder_or_file_name: str) -> None:
        utils.raise_exception_if_true(
            item=not folder_or_file_list,
            on_error_message=f"Object with name: '{folder_or_file_name}' doesnt exist",
            status_code=status.HTTP_404_NOT_FOUND
        )
