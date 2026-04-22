from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

# This tells Google what your app is allowed to do
# 'modify' means it can read emails and edit them to reflect that it's been read or sumn like that
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None

    # If a token already exists from a previous login, load it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token so you don't have to log in every time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("Authentication successful!")
    return creds

authenticate()