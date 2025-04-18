from fastapi import FastAPI, Request
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib

# Initialize the app
app = FastAPI()

# Load the trained model and scaler
model = joblib.load("xgb_model.pkl")
scaler = joblib.load("scaler.pkl")

# Define the input schema
class InputData(BaseModel):
    data: list[list[float]]  # list of rows, each row is a list of features

@app.get("/")
def home():
    return {"message": "Calorie Prediction API is running!"}

@app.post("/predict/")
def predict(input_data: InputData):
    # Convert to DataFrame
    df = pd.DataFrame(input_data.data)

    # Scale the data
    scaled_data = scaler.transform(df)

    # Predict
    prediction = model.predict(scaled_data)

    return {"Predicted Calories": prediction.tolist()}
