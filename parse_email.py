import re

def extract_transaction(email_body):
    transaction = {
        'type': None,
        'amount': None,
        'description': None
    }

    # --- Extract amount and type ---
    # Matches patterns like: 1,000.00 DR  or  50,000.00 CR
    amount_pattern = r'Amount:\s*([\d,]+\.\d{2})\s*(DR|CR)'
    match = re.search(amount_pattern, email_body, re.IGNORECASE)

    if match:
        raw_amount = match.group(1).replace(',', '')
        transaction['amount'] = float(raw_amount)

        dr_cr = match.group(2).upper()
        if dr_cr == 'DR':
            transaction['type'] = 'debit'
        else:
            transaction['type'] = 'credit'

    # --- Extract description from Narration line ---
    # Matches: "Narration: POS TRAN-WEMA POS/LA/NG/20042026"
    desc_match = re.search(r'Narration:\s*(.+)', email_body)
    if desc_match:
        transaction['description'] = desc_match.group(1).strip()

    return transaction