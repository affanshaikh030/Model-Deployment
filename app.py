import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Churn Predictor", page_icon="📈", layout="wide")

# 2. Styling with CSS (The "Pro" touch)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Customer Churn Analysis")
st.write("Optimize your retention strategy with real-time churn predictions.")

# 3. Sidebar for Inputs
with st.sidebar:
    st.header("Input Parameters")
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    charges = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)
    contract = st.selectbox("Contract Type", ["month-to-month", "one-year", "two-year"])
    predict_btn = st.button("Analyze Risk")

# 4. Main Display Area
col1, col2 = st.columns([1, 2])

with col1:
    st.info("Ensure all input parameters are accurate before running the analysis.")

with col2:
    if predict_btn:
        with st.spinner("Analyzing data..."):
            payload = {
                "tenure_months": tenure,
                "monthly_charges": charges,
                "contract_type": contract,
                "support_tickets_raised": 0
            }
            
try:
            response = requests.post("https://model-deployment-tlz1.onrender.com/predict", json=payload)
            
            # This is the "Success" path
            if response.status_code == 200:
                result = response.json()
                probability = result.get('churn_probability', 0)
                tier = result.get('risk_assessment_tier', 'Unknown')
                st.metric(label="Churn Probability", value=f"{probability:.2%}")
                st.write(f"Risk Tier: **{tier}**")
                st.success("Analysis Complete")
            
            # This is the "Failure" path (API connection exists, but error occurred)
            else:
                st.error("API Connection Error. Please check your network.")
                
        # This is the "Safety Net"
except Exception as e:
            st.error(f"Error: {e}")            