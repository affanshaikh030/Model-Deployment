Customer Churn Risk Prediction API
A production-ready machine learning API designed to predict customer churn in real-time. This project demonstrates the full lifecycle of an ML model: from data preprocessing and training to containerized deployment on the cloud.
🚀 The Business Problem
Customer churn is a critical challenge for service-based businesses. By accurately predicting which customers are at risk of leaving, businesses can proactively offer personalized retention strategies, reducing acquisition costs and stabilizing revenue.
🛠 Tech Stack
Language: Python 3.10
API Framework: FastAPI (Chosen for high-performance and automatic documentation)
ML Library: Scikit-Learn
Deployment: Render (Cloud PaaS)
Version Control: Git & GitHub
🌐 Live API
The API is currently live and accessible. You can test the model's predictions by visiting the interactive documentation:
👉 Access the API Swagger UI
How to use the API:
Navigate to the link above.
Expand the POST /predict endpoint.
Click "Try it out".
Input the customer profile (Tenure, Charges, Contract Type, Support Tickets).
Execute to receive the churn probability and risk tier.
🏗 Project Architecture
The project follows a standard production pipeline:
Data Pipeline: Pre-processing input data using a serialized Scikit-Learn pipeline.
Inference Engine: A trained model (exported via joblib) evaluates the input features.
API Layer: FastAPI wraps the model, providing input validation and JSON output.
CI/CD: Automated deployment via GitHub and Render integration.
🔮 Future Roadmap
[ ] Logging: Implement structured logging to store prediction history in a database for future model retraining.
[ ] Validation: Add Pydantic constraints to strictly validate input ranges (e.g., tenure_months >= 0).
[ ] Scalability: Migrate the API into a Docker container for platform-agnostic portability.
📝 Author
[Affan Shaikh] Data Science Practitioner | ML Engineering | [GitHub Profile Link - https://github.com/affanshaikh030]