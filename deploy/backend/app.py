from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from preprocessing import preprocess_data 
from joblib import load
from fastapi.middleware.cors import CORSMiddleware

# Load the preprocessing pipeline and model
preprocessing_pipeline = load("preprocessing_pipeline.joblib")
global_model = load("xgb_model.joblib")

# Initialize FastAPI app
app = FastAPI()

# Allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://m4-weekly-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema for the /predict endpoint
class PredictionRequest(BaseModel):
    start_date: str  # Start date in "YYYY-MM-DD" format
    target_values: list[float]  # List of historical target values

# Healthcheck endpoint
@app.get("/healthcheck")
def healthcheck():
    return {"status": "API is up and running"}

# Prediction endpoint
@app.post("/predict")
def predict(data: PredictionRequest):
    # Parse input data
    start_date = data.start_date
    target_values = data.target_values

    # Validate input
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid start_date format. Use YYYY-MM-DD."}

    if len(target_values) == 0:
        return {"error": "target_values cannot be empty."}

    # Create a DataFrame from input data
    timestamps = pd.date_range(start=start_date, periods=len(target_values), freq="W")
    input_df = pd.DataFrame({"timestamp": timestamps, "target": target_values})

    # Apply preprocessing
    processed_data = preprocessing_pipeline.transform(input_df)

    # Iterative predictions
    predictions = []
    current_data = processed_data.copy()  # Start with the processed input data

    for i in range(5):  # Predict for the next 5 weeks
        next_prediction = global_model.predict(current_data[-1:])  # Predict using the last row
        next_date = timestamps[-1] + timedelta(weeks=1)  # Get the next timestamp
        predictions.append({"date": next_date.strftime("%Y-%m-%d"), "prediction": float(next_prediction[0])})
        
        # Update `current_data` with the new prediction
        next_row = np.append(current_data.iloc[-1, 1:], next_prediction[0])  # Shift and add the new prediction
        current_data = pd.DataFrame([next_row], columns=current_data.columns)  # Update DataFrame
        timestamps = timestamps.append(pd.DatetimeIndex([next_date]))  # Extend timestamps

    return {"predictions": predictions}