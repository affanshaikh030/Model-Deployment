# train.py
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

print("Generating synthetic real-world customer churn dataset...")

# 1. Simulate historical database records
np.random.seed(42)
n_samples = 2000

data = pd.DataFrame({
    'tenure_months': np.random.randint(1, 72, n_samples),
    'monthly_charges': np.random.uniform(20.0, 120.0, n_samples),
    'contract_type': np.random.choice(['month-to-month', 'one-year', 'two-year'], n_samples),
    'support_tickets_raised': np.random.randint(0, 10, n_samples)
})

# Create a realistic target variable (higher charges + more support tickets = higher churn risk)
churn_prob = 1 / (1 + np.exp(-(-2 + 0.04 * data['support_tickets_raised'] + 0.01 * data['monthly_charges'] - 0.05 * data['tenure_months'])))
data['churn'] = (churn_prob > np.random.uniform(0, 1, n_samples)).astype(int)

# 2. Separate features and target
X = data.drop(columns=['churn'])
y = data['churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Define preprocessing for mixed data types
numerical_features = ['tenure_months', 'monthly_charges', 'support_tickets_raised']
categorical_features = ['contract_type']

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# 4. Bundle preprocessing and the model into a unified pipeline
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(random_state=42))
])

# 5. Train the entire pipeline
print("Training the production pipeline...")
full_pipeline.fit(X_train, y_train)

# Evaluate
accuracy = full_pipeline.score(X_test, y_test)
print(f"Pipeline trained successfully. Evaluation Accuracy: {accuracy * 100:.2f}%")

# 6. Save the entire pipeline artifact inside the app folder
os.makedirs("app", exist_ok=True)
artifact_path = "app/churn_pipeline.joblib"
joblib.dump(full_pipeline, artifact_path)
print(f"Unified pipeline artifact exported securely to: {artifact_path}")