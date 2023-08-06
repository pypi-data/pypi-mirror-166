import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime

SCOPE = ['https://www.googleapis.com/auth/presentations.readonly']
PATH_TO_CREDENTIALS = 'API/token.json'  # The file token.json stores the user's access and refresh tokens
try:
    credentials = None
    if os.path.exists(PATH_TO_CREDENTIALS):
        credentials = Credentials.from_authorized_user_file(PATH_TO_CREDENTIALS, SCOPE)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('API/credentials.json', SCOPE)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(PATH_TO_CREDENTIALS, 'w') as token:
            token.write(credentials.to_json())
except Exception as e:
    raise ConnectionError('There is an issue with the credentials ' + str(e))


def get_presentation(presentation_id='19Fh8FULu6hNFVpb5iK6-NrBNqin3SLozE0emdJtstPM'):
    """Description: Calls the google slides API and returns the presentation based on the presentation ID
    Input:
        1) presentation_id : the google presentation id found on the url
    Returns:
        The presentation in json format
    """
    try:
        service = build('slides', 'v1', credentials=credentials)
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        return presentation
    except Exception as e:
        raise ConnectionError('Cannot retrieve slides due to ' + str(e))

if __name__ == '__main__':
    get_presentation()
