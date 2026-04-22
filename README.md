# BankReceiptTracker

A desktop app that automatically reads FirstBank alert emails from Gmail 
and logs transactions into an Excel spreadsheet with a running balance.

## Features
- Connects to Gmail via Google API
- Parses debit/credit alerts from FirstBank emails
- Logs to Excel with date, narration, type, amount, and balance
- Marks emails as read after processing
- Runs automatically via Windows Task Scheduler

## Setup

### 1. Clone the repo
git clone https://github.com/yourusername/BankReceiptTracker.git

### 2. Install dependencies
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openpyxl

### 3. Add your credentials
- Go to Google Cloud Console
- Enable Gmail API
- Download OAuth credentials as `credentials.json`
- Place it in the project root

### 4. Run
python read_emails.py"# BankReceiptTracker" 
