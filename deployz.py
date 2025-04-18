from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load the saved model
model = joblib.load("xgb_model.pkl")

@app.get("/")
def home():
    return {"message": "Calorie Prediction API is running!"}

@app.post("/predict/")
def predict(features: list):
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    return {"Predicted Calories": prediction.tolist()}
