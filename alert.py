# alert.py  —  automated email alert system

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_fraud_alert(transaction_id, amount, fraud_probability,
                      sender_email, sender_password, recipient_email):
    """Send an email alert when a fraudulent transaction is detected."""

    subject = f'FRAUD ALERT: Suspicious Transaction Detected'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    body = f'''
    FRAUD DETECTION ALERT
   
    Time         : {timestamp}
    Transaction  : {transaction_id}
    Amount       : ${amount:.2f}
    Fraud Score  : {fraud_probability*100:.1f}%
    Status       : BLOCKED - Pending Review

    Please review this transaction immediately.
    '''

    msg = MIMEMultipart()
    msg['From']    = sender_email
    msg['To']      = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f'Alert sent to {recipient_email}')
    except Exception as e:
        print(f'Failed to send alert: {e}')


