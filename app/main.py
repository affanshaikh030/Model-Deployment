# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

app = FastAPI(
    title="Enterprise Customer Churn Risk API",
    description="Production API endpoint evaluating real-time customer risk profiles.",
    version="2.0"
)

# Locate and safely load the unified pipeline artifact
ARTIFACT_PATH = os.path.join(os.path.dirname(__file__), "churn_pipeline.joblib")

try:
    model_pipeline = joblib.load(ARTIFACT_PATH)
except Exception as e:
    print(f"Critical Error: Execution halted. Failed to load pipeline artifact. {e}")
    model_pipeline = None

# Define input schema with production data constraints
class CustomerData(BaseModel):
    tenure_months: int = Field(..., ge=0, description="Number of months customer has been active.")
    monthly_charges: float = Field(..., ge=0.0, description="Current monthly bill amount.")
    contract_type: str = Field(..., description="Type of active agreement: 'month-to-month', 'one-year', or 'two-year'.")
    support_tickets_raised: int = Field(..., ge=0, description="Total technical or billing tickets raised.")

    class Config:
        json_schema_extra = {
            "example": {
                "tenure_months": 12,
                "monthly_charges": 89.50,
                "contract_type": "month-to-month",
                "support_tickets_raised": 4
            }
        }

@app.get("/")
def health_check():
    return {"status": "healthy", "model_loaded": model_pipeline is not None}

@app.post("/predict")
def evaluate_churn_risk(customer: CustomerData):
    if model_pipeline  is None:
        raise HTTPException(status_code=500, detail="Inference engine unavailable.")
    
    # 1. Convert incoming JSON request directly into a Pandas DataFrame
    # The pipeline handles scaling and one-hot encoding automatically
    input_df = pd.DataFrame([customer.model_dump()])
    
    try:
        # 2. Extract classification prediction and exact probabilities
        prediction = int(model_pipeline.predict(input_df)[0])
        probabilities = model_pipeline.predict_proba(input_df)[0]
        
        churn_probability = float(probabilities[1])
        
        # 3. Formulate business response logic
        risk_tier = "Low"
        if churn_probability >= 0.7:
            risk_tier = "High"
        elif churn_probability >= 0.4:
            risk_tier = "Medium"

        return {
            "churn_prediction": prediction,
            "churn_probability": round(churn_probability, 4),
            "risk_assessment_tier": risk_tier,
            "action_required": prediction == 1
        }
        
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=f"Data formatting error encountered: {str(val_err)}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Inference pipeline execution failure: {str(err)}")