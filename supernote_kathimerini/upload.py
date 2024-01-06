from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import datetime

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload():
    print('Uploading to Supernote')
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Get today's date and format it as yyyy-mm-dd
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    # Form the file name
    file_name = f'{today}-news.pdf'

    # File metadata
    file_metadata = {
        'name': file_name,
        'parents' : ['1DZg-dlgd9Xivcj6IenJ0A_oBNs7j3MMA'] # This is the id of my Supernote/Document/News folder
    }

    # Use the MediaFileUpload class to upload the file
    media = MediaFileUpload(file_name, mimetype='application/pdf')
    request = service.files().create(
        media_body=media,
        body=file_metadata
    )
    request.execute()

if __name__ == '__main__':
    upload()
