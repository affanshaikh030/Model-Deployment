import requests

# 1. Your Live URL
URL = "https://model-deployment-tlz1.onrender.com/predict"

# 2. Test Data (A mock customer profile)
test_payload = {
    "tenure_months": 12,
    "monthly_charges": 50.0,
    "contract_type": "month-to-month",
    "support_tickets_raised": 0
}

def run_test():
    try:
        print(f"Sending request to {URL}...")
        response = requests.post(URL, json=test_payload)
        
        # 3. Validation Logic
        if response.status_code == 200:
            print("✅ SUCCESS: API is live and responding!")
            print(f"Model Prediction: {response.json()}")
        else:
            print(f"❌ ERROR: API returned status code {response.status_code}")
            
    except Exception as e:
        print(f"❌ FAILED: Could not connect to API. Reason: {e}")

if __name__ == "__main__":
    run_test()