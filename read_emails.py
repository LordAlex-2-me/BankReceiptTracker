import base64
import re
from auth_test import authenticate  # reuse the auth function you already wrote
from parse_email import extract_transaction
from excel_logger import log_transaction

def get_gmail_service():
    creds = authenticate()
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=creds)
    return service


def search_emails(service, query):
    """Search inbox and return a list of message IDs matching the query."""
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])
    return messages


def get_email_body(service, message_id):
    """Fetch the full email and extract its plain text body."""
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()

    payload = message['payload']
    parts = payload.get('parts', [])

    body = ""

    # Some emails are simple (no parts), others are multipart
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    else:
        # Single part email
        data = payload['body'].get('data', '')
        body = base64.urlsafe_b64decode(data).decode('utf-8')

    return body

def mark_as_read(service, message_id):
    """Remove the UNREAD label from a message so it isn't processed again."""
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print(f"Marked email {message_id} as read.")

def fetch_bank_emails():
    service = get_gmail_service()

    # 🔧 CHANGE THIS to match your bank's sender address
    query = "from:FirstAlert@firstbanknigeria.com is:unread"

    messages = search_emails(service, query)

    if not messages:
        print("No new bank emails found.")
        return

    print(f"Found {len(messages)} email(s). Reading...\n")

    for msg in messages:
        body = get_email_body(service, msg['id'])
        transaction = extract_transaction(body)
        print(f"Processing email {msg['id']}...")

        if transaction['amount']:
            log_transaction(transaction)
            mark_as_read(service, msg['id'])
        else:
            print("Could not parse amount — skipping.")

fetch_bank_emails()