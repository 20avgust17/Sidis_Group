from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_google_drive_gauth() -> GoogleDrive:
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")

    return GoogleDrive(gauth)
