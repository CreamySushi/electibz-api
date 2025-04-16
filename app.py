from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib

app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load('xgb_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Expecting a JSON request
    df = pd.DataFrame(data)
    df = scaler.transform(df)
    prediction = model.predict(df)
    return jsonify({'prediction': prediction.tolist()})

import os
model_path = os.path.join(os.path.dirname(__file__), 'xgb_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

model_path = r"C:\Users\Christian\OneDrive - University of Perpetual Help System JONELTA\Desktop\ELECTIBZ\xgb_model.pkl"
scaler_path = r"C:\Users\Christian\OneDrive - University of Perpetual Help System JONELTA\Desktop\ELECTIBZ\scaler.pkl"

# Load the trained model and scaler
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)