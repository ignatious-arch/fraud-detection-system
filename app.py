# app.py
from alert import send_fraud_alert
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib, numpy as np, pandas as pd
import uuid
from datetime import datetime
from database import save_transaction, get_all_transactions, get_stats as db_get_stats

app = FastAPI(title='Fraud Detection API')

FRAUD_THRESHOLD = 0.4

try:
    model         = joblib.load('fraud_model.pkl')
    scaler_time   = joblib.load('scaler_time.pkl')
    scaler_amount = joblib.load('scaler_amount.pkl')
    print('Models loaded successfully!')
except Exception as e:
    print(f'Error loading models: {e}')
    raise

class Transaction(BaseModel):
    Time: float
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount: float

@app.get('/')
def root():
    return JSONResponse(content={'message': 'Fraud Detection API is running'})

@app.get('/logs')
def get_logs():
    transactions = get_all_transactions()
    return JSONResponse(content={
        'total_transactions': len(transactions),
        'total_fraud': sum(1 for t in transactions if t['verdict'] == 'FRAUD'),
        'total_legitimate': sum(1 for t in transactions if t['verdict'] == 'LEGITIMATE'),
        'logs': transactions
    })

@app.get('/stats')
def get_stats():
    import json
    stats = db_get_stats()
    return JSONResponse(content=json.loads(json.dumps(stats, default=str)))

@app.post('/predict')
def predict(transaction: Transaction):
    try:
        transaction_id = f'TXN-{uuid.uuid4().hex[:8].upper()}'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        df = pd.DataFrame([transaction.model_dump()])
        df['Time']   = scaler_time.transform(df[['Time']])
        df['Amount'] = scaler_amount.transform(df[['Amount']])

        proba   = float(model.predict_proba(df.values)[0][1])
        verdict = 'FRAUD' if proba >= FRAUD_THRESHOLD else 'LEGITIMATE'

        # Save to database
        try:
            save_transaction(
                transaction_id=transaction_id,
                timestamp=timestamp,
                amount=float(transaction.Amount),
                fraud_probability=proba,
                verdict=verdict,
                v14=float(transaction.V14),
                v4=float(transaction.V4),
                v12=float(transaction.V12)
            )
            print(f'Transaction {transaction_id} saved successfully')
        except Exception as e:
            print(f'Database error: {e}')

        # Send alert if fraud detected
        if verdict == 'FRAUD':
            try:
                send_fraud_alert(
                    transaction_id=transaction_id,
                    amount=float(transaction.Amount),
                    fraud_probability=proba,
                    sender_email='ignatiousmaunga@gmail.com',
                    sender_password='runjalmchczzvbxg',
                    recipient_email='ignatiousmunyaradzi75@gmail.com'
                )
            except Exception as e:
                print(f'Alert error: {e}')

        return JSONResponse(content={
            'transaction_id': transaction_id,
            'timestamp': timestamp,
            'fraud_probability': round(proba, 4),
            'verdict': verdict,
            'confidence': f'{proba*100:.1f}%'
        })
    except Exception as e:
        print(f'Predict error: {e}')
        return JSONResponse(content={'error': str(e)}, status_code=500)