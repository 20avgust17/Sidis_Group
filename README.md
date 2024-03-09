Set up project.
1. Pull the main branch to the local repository.
2. Install file mycreds.txt to SidisBackend folder (I'll send HR).
3. In Pycharm terminal run the command "pip install -r requirements.local.txt".
4. Run the command "uvicorn src.main:app --host localhost".
5. To view interface use url http://localhost:8000/v1/google_drive_files/index/ (Only for 1 endpoint).
6. To view api use url - http://localhost:8000/docs#/ (All endpoinds with docs by swagger).

Possible improvements:
1. Add dependency injections to endpoints on getting a file or folder.
2. Finish writing the application interface.
3. Rewrite backgroud tasks to full-fledged Rabbitmq or Celery queues.
4. Add a separate api for working with folders in Google drive.
5. Write tests for the endpoints.
6. Extend swager documentation and add custom error output.
7. Possibly a departure from the pydrive library.


In case of any problems with the access token, please contact me via hr. Good luck!
