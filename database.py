# database.py
import pymysql
from datetime import datetime
import os

def get_connection():
    host = os.getenv('MYSQLHOST', 'localhost')
    user = os.getenv('MYSQLUSER', 'root')
    password = os.getenv('MYSQLPASSWORD', 'fraud123')
    database = os.getenv('MYSQLDATABASE', 'fraud_detection')
    port = int(os.getenv('MYSQLPORT', '3306'))
    
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        cursorclass=pymysql.cursors.DictCursor
    )

def save_transaction(transaction_id, timestamp, amount,
                     fraud_probability, verdict, v14=None, v4=None, v12=None):
    """Save a transaction to the MySQL database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO transactions 
                (transaction_id, timestamp, amount, fraud_probability, verdict, v14, v4, v12)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            str(transaction_id),
            str(timestamp),
            float(amount),
            float(fraud_probability),
            str(verdict),
            float(v14) if v14 is not None else None,
            float(v4) if v4 is not None else None,
            float(v12) if v12 is not None else None
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        print(f'Transaction {transaction_id} saved to MySQL.')
    except Exception as e:
        print(f'Error saving transaction: {e}')

def get_all_transactions():
    """Get all transactions from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY id DESC')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_stats():
    """Get fraud statistics from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN verdict = 'FRAUD' THEN 1 ELSE 0 END) as total_fraud,
            SUM(CASE WHEN verdict = 'LEGITIMATE' THEN 1 ELSE 0 END) as total_legitimate,
            AVG(fraud_probability) as avg_probability,
            AVG(CASE WHEN verdict = 'FRAUD' THEN amount ELSE NULL END) as avg_fraud_amount
        FROM transactions
    ''')
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    total = int(row.get('total') or 0)
    fraud = int(row.get('total_fraud') or 0)
    legit = int(row.get('total_legitimate') or 0)
    return {
        'total_transactions': total,
        'total_fraud': fraud,
        'total_legitimate': legit,
        'fraud_percentage': round((fraud / total) * 100, 2) if total > 0 else 0,
        'average_fraud_probability': round(float(row.get('avg_probability') or 0), 4),
        'average_fraud_amount': round(float(row.get('avg_fraud_amount') or 0), 2)
    }

def get_fraud_transactions():
    """Get only fraudulent transactions."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions 
        WHERE verdict = 'FRAUD' 
        ORDER BY fraud_probability DESC
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def search_transactions(min_amount=None, max_amount=None, verdict=None):
    """Search transactions by amount range or verdict."""
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM transactions WHERE 1=1'
    params = []
    if min_amount is not None:
        query += ' AND amount >= %s'
        params.append(min_amount)
    if max_amount is not None:
        query += ' AND amount <= %s'
        params.append(max_amount)
    if verdict is not None:
        query += ' AND verdict = %s'
        params.append(verdict)
    query += ' ORDER BY id DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

print("MySQL Database ready.")