# monitor.py
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from database import get_stats, get_all_transactions

# Settings
FRAUD_RATE_MIN = 0.1      # alert if fraud rate drops below 10%
FRAUD_RATE_MAX = 90.0     # alert if fraud rate exceeds 90%
MIN_TRANSACTIONS = 10     # minimum transactions needed before monitoring kicks in
LOW_CONFIDENCE_THRESHOLD = 0.6  # alert if average confidence drops below 60%

SENDER_EMAIL    = 'ignatiousmaunga@gmail.com'
SENDER_PASSWORD = 'runjalmchczzvbxg'
RECIPIENT_EMAIL = 'ignatiousmunyaradzi75@gmail.com'

def send_monitor_alert(subject, body):
    """Send a monitoring alert email."""
    msg = MIMEMultipart()
    msg['From']    = SENDER_EMAIL
    msg['To']      = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print(f'Monitor alert sent: {subject}')
    except Exception as e:
        print(f'Failed to send monitor alert: {e}')

def check_fraud_rate():
    """Check if fraud rate is within normal range."""
    stats = get_stats()
    total = stats['total_transactions']

    if total < MIN_TRANSACTIONS:
        print(f'Not enough transactions yet ({total}/{MIN_TRANSACTIONS}). Skipping check.')
        return

    fraud_rate = stats['fraud_percentage']
    print(f'Current fraud rate: {fraud_rate}%')

    if fraud_rate < FRAUD_RATE_MIN:
        send_monitor_alert(
            subject='⚠️ MONITOR ALERT: Fraud Rate Unusually Low',
            body=f'''
MODEL MONITORING ALERT

Time        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Issue       : Fraud rate is unusually LOW
Current Rate: {fraud_rate}%
Expected    : Above {FRAUD_RATE_MIN}%
Transactions: {total}

This may indicate the model is missing fraud cases.
Please review recent transactions and consider retraining.
            '''
        )

    elif fraud_rate > FRAUD_RATE_MAX:
        send_monitor_alert(
            subject='⚠️ MONITOR ALERT: Fraud Rate Unusually High',
            body=f'''
MODEL MONITORING ALERT

Time        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Issue       : Fraud rate is unusually HIGH
Current Rate: {fraud_rate}%
Expected    : Below {FRAUD_RATE_MAX}%
Transactions: {total}

This may indicate too many false positives.
Please review recent transactions and consider retraining.
            '''
        )
    else:
        print(f'Fraud rate is normal: {fraud_rate}%')

def check_confidence():
    """Check if model confidence is high enough."""
    transactions = get_all_transactions()

    if len(transactions) < MIN_TRANSACTIONS:
        print(f'Not enough transactions yet. Skipping confidence check.')
        return

    avg_confidence = sum(t['fraud_probability'] for t in transactions) / len(transactions)
    print(f'Average model confidence: {avg_confidence:.4f}')

    if avg_confidence < LOW_CONFIDENCE_THRESHOLD:
        send_monitor_alert(
            subject='⚠️ MONITOR ALERT: Model Confidence Dropping',
            body=f'''
MODEL MONITORING ALERT

Time              : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Issue             : Model confidence is LOW
Average Confidence: {avg_confidence:.4f}
Expected          : Above {LOW_CONFIDENCE_THRESHOLD}
Transactions      : {len(transactions)}

The model may be uncertain about recent transactions.
Consider retraining with newer data.
            '''
        )
    else:
        print(f'Model confidence is healthy: {avg_confidence:.4f}')

def check_transaction_volume():
    """Check if transaction volume has dropped suddenly."""
    transactions = get_all_transactions()

    if len(transactions) < 2:
        print('Not enough transactions to check volume.')
        return

    # Get transactions from last hour
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)

    recent = [
        t for t in transactions
        if datetime.strptime(t['timestamp'], '%Y-%m-%d %H:%M:%S') >= one_hour_ago
    ]

    print(f'Transactions in last hour: {len(recent)}')

    if len(recent) == 0:
        print('No transactions in the last hour — system may be idle.')

def generate_health_report():
    """Generate a full health report of the system."""
    stats = get_stats()
    transactions = get_all_transactions()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print('\n' + '='*50)
    print('FRAUD DETECTION SYSTEM — HEALTH REPORT')
    print('='*50)
    print(f'Report Time          : {timestamp}')
    print(f'Total Transactions   : {stats["total_transactions"]}')
    print(f'Total Fraud          : {stats["total_fraud"]}')
    print(f'Total Legitimate     : {stats["total_legitimate"]}')
    print(f'Fraud Rate           : {stats["fraud_percentage"]}%')
    print(f'Avg Fraud Probability: {stats["average_fraud_probability"]}')
    print(f'Avg Fraud Amount     : ${stats["average_fraud_amount"]}')
    print('='*50 + '\n')

    # Run all checks
    check_fraud_rate()
    check_confidence()
    check_transaction_volume()

    print('\nHealth check complete.')

# Run the health report when this file is executed
if __name__ == '__main__':
    generate_health_report()