# 🔍 Credit Card Fraud Detection System

A production-grade, end-to-end machine learning system that detects fraudulent credit card transactions in real time. Built with XGBoost, FastAPI, MySQL, and Streamlit — fully deployed to the cloud.

**Live API:** [https://web-production-4181.up.railway.app](https://web-production-4181.up.railway.app)  
**API Docs:** [https://web-production-4181.up.railway.app/docs](https://web-production-4181.up.railway.app/docs)



## 📌 Project Overview

This system was built to detect fraudulent credit card transactions using machine learning. It was trained on a dataset of 284,807 real European credit card transactions and achieves near-perfect fraud detection accuracy. The system is fully deployed to the cloud and runs 24/7 without any manual intervention(for a numbered of days).



## 🏗️ System Architecture


Transaction Data
      ↓
FastAPI REST API (Railway Cloud)
      ↓
XGBoost ML Model
      ↓
Fraud Probability Score
      ↓
├── Save to MySQL Database (Railway)
├── Send Email Alert (if FRAUD)
└── Return Verdict to Caller




## ✨ Features

- **Real-Time Fraud Detection** — scores any transaction in milliseconds with up to 100% confidence
- **Machine Learning Model** — XGBoost classifier trained on 284,807 transactions
- **REST API** — FastAPI endpoints accessible from anywhere in the world
- **Cloud MySQL Database** — every transaction permanently stored on Railway
- **Automated Email Alerts** — instant Gmail notification when fraud is detected
- **Interactive Dashboard** — Streamlit visual interface with charts and transaction history
- **Model Monitoring** — automated health checks and performance tracking
- **Model Explainability** — SHAP values show exactly why a transaction was flagged

---

## 🧠 Machine Learning

### Dataset
- **Source:** Kaggle Credit Card Fraud Detection Dataset
- **Size:** 284,807 transactions over 2 days
- **Features:** 30 features (V1-V28 PCA components, Time, Amount)
- **Class imbalance:** Only 0.17% fraud — handled with SMOTE

### Models Trained & Compared

| Model | Precision | Recall | F1 Score | AUC-PR |

| Logistic Regression | ~0.85 | ~0.62 | ~0.72 | ~0.74 |
| Random Forest | ~0.95 | ~0.80 | ~0.87 | ~0.86 |
| **XGBoost** | **~0.96** | **~0.84** | **~0.90** | **~0.91** |

### Key Techniques
- SMOTE for handling class imbalance
- Stratified K-Fold cross-validation
- Threshold tuning for business cost optimisation
- SHAP explainability for regulatory compliance


## 🚀 API Endpoints

| Endpoint | Method | Description |

| `/` | GET | Check API status |
| `/predict` | POST | Score a transaction |
| `/stats` | GET | View fraud statistics |
| `/logs` | GET | View transaction history |
| `/docs` | GET | Interactive API documentation |

### Example Request

```python
import requests

transaction = {
    "Time": 406,
    "V1": -2.31, "V2": 1.95, "V3": -1.60, "V4": 3.99,
    # ... V5 through V28
    "Amount": 239.93
}

response = requests.post(
    "https://web-production-4181.up.railway.app/predict",
    json=transaction
)
print(response.json())
```

### Example Response

```json
{
    "transaction_id": "TXN-A7EE9623",
    "timestamp": "2026-04-25 10:04:11",
    "fraud_probability": 1.0,
    "verdict": "FRAUD",
    "confidence": "100.0%"
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |

| Machine Learning | XGBoost, Scikit-learn, SHAP |
| Data Processing | Pandas, NumPy |
| Class Balancing | SMOTE (imbalanced-learn) |
| API Framework | FastAPI |
| API Server | Uvicorn |
| Database | MySQL (Railway Cloud) |
| Dashboard | Streamlit, Plotly |
| Email Alerts | Python smtplib (Gmail) |
| Deployment | Railway |
| Version Control | GitHub |
| Language | Python 3.11 |



## 📁 Project Structure


fraud-detection-system/
├── app.py              # FastAPI application and endpoints
├── database.py         # MySQL database connection and queries
├── dashboard.py        # Streamlit visual dashboard
├── alert.py            # Automated email alert system
├── monitor.py          # Model health monitoring
├── requirements.txt    # Python dependencies
├── Procfile            # Railway deployment configuration
├── fraud_model.pkl     # Trained XGBoost model
├── scaler_time.pkl     # Time feature scaler
└── scaler_amount.pkl   # Amount feature scaler




## 📊 Dashboard Features

- **System Statistics** — total transactions, fraud count, fraud rate
- **Quick Test Buttons** — test fraud and legitimate transactions instantly
- **Transaction History Table** — colour-coded red/green by verdict
- **Fraud vs Legitimate Pie Chart** — visual breakdown
- **Fraud Probability Bar Chart** — per-transaction scores



## ☁️ Cloud Deployment

The system is deployed on **Railway** with two services:

1. **Web Service** — FastAPI application serving the REST API
2. **MySQL Service** — Cloud database storing all transactions permanently

The system runs 24/7 without any manual intervention. Any transaction sent to the API is automatically scored, stored, and alerted on if fraudulent.



## 🔧 Running Locally

```bash
# Clone the repository
git clone https://github.com/ignatious-arch/fraud-detection-system.git
cd fraud-detection-system

# Create virtual environment with Python 3.11
py -3.11 -m venv venv311
venv311\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app:app --reload

# In a second terminal, start the dashboard
streamlit run dashboard.py




## 📈 Results

- **Fraud Detection Rate:** ~84% (Recall)
- **Precision:** ~96% (very few false alarms)
- **AUC-PR:** ~0.91 (industry standard metric for imbalanced fraud data)
- **Response Time:** < 100ms per transaction
- **Uptime:** 24/7 on Railway cloud

---

## 👤 Author

**Ignatious Munyaradzi Maunga**  
Built as part of a machine learning and full-stack deployment portfolio project.

---

## 📄 License

This project is for portfolio and educational purposes.
