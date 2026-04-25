# dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title(" Credit Card Fraud Detection System")
st.markdown("Real-time fraud detection powered by XGBoost machine learning")
st.divider()

# API URL
API_URL = "http://127.0.0.1:8000"

# Section 1 - Stats at the top
st.subheader("📊 System Statistics")

try:
    stats = requests.get(f"{API_URL}/stats").json()
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", stats['total_transactions'])
    col2.metric("Fraud Detected", stats['total_fraud'], delta="🚨")
    col3.metric("Legitimate", stats['total_legitimate'], delta="✅")
    col4.metric("Fraud Rate", f"{stats['fraud_percentage']}%")

except:
    st.warning("API is not running. Start uvicorn first.")

st.divider()

# Section 2 - Test a transaction
st.subheader("💳 Test a Transaction")

col_left, col_right = st.columns(2)

with col_left:
    amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=239.93)
    time = st.number_input("Time (seconds since first transaction)", min_value=0.0, value=406.0)

with col_right:
    st.info("V1-V28 are anonymized PCA features from the dataset. Use preset transactions below to test.")

st.markdown("**Quick Test Buttons:**")
col_fraud, col_legit = st.columns(2)

# Preset fraud transaction
fraud_data = {
    'Time':406,'V1':-2.31,'V2':1.95,'V3':-1.60,'V4':3.99,'V5':-0.52,
    'V6':-1.42,'V7':-2.53,'V8':1.39,'V9':-2.77,'V10':-2.77,'V11':3.20,
    'V12':-2.89,'V13':-0.59,'V14':-4.28,'V15':0.38,'V16':-1.14,'V17':-2.83,
    'V18':-0.01,'V19':0.41,'V20':0.12,'V21':0.51,'V22':-0.03,'V23':-0.46,
    'V24':0.32,'V25':0.04,'V26':0.17,'V27':0.26,'V28':-0.14,'Amount':239.93
}

# Preset legitimate transaction
legit_data = {
    'Time':52000,'V1':1.19,'V2':0.26,'V3':0.16,'V4':0.44,'V5':0.06,
    'V6':-0.08,'V7':-0.07,'V8':0.08,'V9':-0.25,'V10':-0.16,'V11':1.61,
    'V12':1.06,'V13':0.48,'V14':-0.14,'V15':0.63,'V16':0.46,'V17':-0.11,
    'V18':-0.18,'V19':-0.14,'V20':-0.06,'V21':-0.22,'V22':-0.63,'V23':0.10,
    'V24':-0.33,'V25':0.16,'V26':0.12,'V27':-0.008,'V28':0.014,'Amount':2.69
}

with col_fraud:
    if st.button("🚨 Test Fraud Transaction", use_container_width=True):
        with st.spinner("Analysing transaction..."):
            response = requests.post(f"{API_URL}/predict", json=fraud_data)
            result = response.json()
        st.error(f"🚨 VERDICT: {result['verdict']}")
        st.metric("Fraud Probability", result['confidence'])
        st.write(f"Transaction ID: `{result['transaction_id']}`")
        st.write(f"Timestamp: `{result['timestamp']}`")

with col_legit:
    if st.button("✅ Test Legitimate Transaction", use_container_width=True):
        with st.spinner("Analysing transaction..."):
            response = requests.post(f"{API_URL}/predict", json=legit_data)
            result = response.json()
        st.success(f"✅ VERDICT: {result['verdict']}")
        st.metric("Fraud Probability", result['confidence'])
        st.write(f"Transaction ID: `{result['transaction_id']}`")
        st.write(f"Timestamp: `{result['timestamp']}`")

st.divider()

# Section 3 - Transaction history
st.subheader("📋 Transaction History")

try:
    logs = requests.get(f"{API_URL}/logs").json()

    if logs['total_transactions'] == 0:
        st.info("No transactions yet. Test one above!")
    else:
        df = pd.DataFrame(logs['logs'])

        def colour_verdict(val):
            color = 'red' if val == 'FRAUD' else 'green'
            return f'color: {color}; font-weight: bold'

        st.dataframe(
            df.style.map(colour_verdict, subset=['verdict']),
            use_container_width=True
        )

        st.divider()

        # Section 4 - Charts
        st.subheader("📈 Fraud Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            verdict_counts = df['verdict'].value_counts().reset_index()
            verdict_counts.columns = ['Verdict', 'Count']
            fig1 = px.pie(
                verdict_counts,
                values='Count',
                names='Verdict',
                title='Fraud vs Legitimate Transactions',
                color='Verdict',
                color_discrete_map={'FRAUD': 'red', 'LEGITIMATE': 'green'}
            )
            st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            fig2 = px.bar(
                df,
                x='transaction_id',
                y='fraud_probability',
                color='verdict',
                title='Fraud Probability per Transaction',
                color_discrete_map={'FRAUD': 'red', 'LEGITIMATE': 'green'}
            )
            fig2.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Could not load logs: {e}")

st.divider()
st.caption("Credit Card Fraud Detection System | Powered by XGBoost + FastAPI + Streamlit")