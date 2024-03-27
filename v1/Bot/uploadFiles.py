from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import sys
import magic

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']

folder_id = ""

def downloadFile(url):
    os.system(f"wget --no-check-certificate {url} -P ./data/")
    g_link = uploadFiles(url.split("/")[-1], url)
    return g_link

def uploadFiles(fileName, url):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./creds/token.json'):
        creds = Credentials.from_authorized_user_file('./creds/token.json', SCOPES)
    
    # if this file isnt there this may be a heroku instance
    elif os.path.exists('/app/google-credentials.json'):
        creds = Credentials.from_authorized_user_file('/app/google-credentials.json', SCOPES)
    else:
        print("Please run upload upload.py before using it!!!")
        sys.exit(1)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    file_metadata = {
        "name": fileName,
        "parents": [folder_id]
    }
    path = "./data/{}".format(fileName)
    media = MediaFileUpload(path, mimetype=giveMimeType(fileName))
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    with open("dataUploaded.txt", "a+") as log:
        # Move read cursor to the start of file.
        log.seek(0)
        # If file is not empty then append '\n'
        data = log.read(100)
        if len(data) > 0 :
            log.write("\n")
        # Append text at the end of file
        log.write(url)

    link = f"https://drive.google.com/file/d/{file.get('id')}"
    os.system("rm ./data/*")
    return link

def giveMimeType(file):
    mime = magic.Magic(mime=True)
    return mime.from_file(f"./data/{file}")
try:
    print(os.environ['GDRIVE_FOLDER'])
    folder_id = str(os.environ['GDRIVE_FOLDER'])

except:
    print("Invalid folder id")