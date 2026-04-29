import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None

    # Try reading token from environment variable first (GitHub Actions)
    token_env = os.environ.get('GMAIL_TOKEN')
    credentials_env = os.environ.get('GMAIL_CREDENTIALS')

    if token_env:
        # Running on GitHub Actions — load token from environment
        token_data = json.loads(token_env)

        creds = Credentials(
            token=token_data.get('token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret'),
            scopes=token_data.get('scopes')
        )

    elif os.path.exists('token.json'):
        # Running locally — load token from file as before
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Refresh the token if it's expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

        # If running on GitHub, update the environment with refreshed token
        # (token.json won't persist between runs anyway)
        if not os.path.exists('token.json'):
            print("Token refreshed successfully.")

    if not creds or not creds.valid:
        raise Exception(
            "No valid credentials found. "
            "Run the app locally first to generate token.json, "
            "then update the GMAIL_TOKEN secret on GitHub."
        )

    print("Authentication successful!")
    return creds