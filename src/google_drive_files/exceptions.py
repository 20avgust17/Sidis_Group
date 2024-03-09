class InvalidUploadFile(Exception):
    """Exception raised when there is an issue with uploading a file to Google Drive."""


class InvalidUpdateFile(Exception):
    """Exception raised when there is an issue with updating a file on Google Drive."""


class InvalidMoveFile(Exception):
    """Exception raised when there is an issue with moving a file on Google Drive."""


class InvalidDeleteFile(Exception):
    """Exception raised when there is an issue with deleting a file from Google Drive."""


class InvalidExecutionRequest(Exception):
    """Exception raised when an invalid execution request is made."""
