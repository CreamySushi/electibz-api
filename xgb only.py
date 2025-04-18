import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

import warnings
warnings.filterwarnings('ignore')

# Load data
df1 = pd.read_csv('exercise.csv')
df2 = pd.read_csv('calories.csv')

# Merge and preprocess data
merge_data = pd.merge(df1, df2, how='outer')
merge_data.replace({'male': 0, 'female': 1}, inplace=True)
print(merge_data)

# Define features and target
features = merge_data.drop(['User_ID', 'Calories'], axis=1)
target = merge_data['Calories'].values

# Split data
X_train, X_val, Y_train, Y_val = train_test_split(features, target, test_size=0.1, random_state=22)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# Train XGBRegressor
model = XGBRegressor()
model.fit(X_train, Y_train)

# Predictions and evaluation
train_preds = model.predict(X_train)
val_preds = model.predict(X_val)

print("XGBRegressor:")
print("Training Error (MAE):", mean_absolute_error(Y_train, train_preds))
print("Validation Error (MAE):", mean_absolute_error(Y_val, val_preds))
print("Training RMSE:", np.sqrt(mean_squared_error(Y_train, train_preds)))
print("Validation RMSE:", np.sqrt(mean_squared_error(Y_val, val_preds)))
print("Training R-squared:", r2_score(Y_train, train_preds))
print("Validation R-squared:", r2_score(Y_val, val_preds))


import joblib

# Save the model
joblib.dump(model, 'xgb_model.pkl')

# Load the model (for testing or deployment)
loaded_model = joblib.load('xgb_model.pkl')

joblib.dump(scaler, 'scaler.pkl')
loaded_scaler = joblib.load('scaler.pkl')


# Data visualization
sb.scatterplot(x='Height', y='Weight', data=merge_data)

features = ['Age', 'Height', 'Weight', 'Duration']
plt.subplots(figsize=(15, 10))
for i, col in enumerate(features):
    plt.subplot(2, 2, i + 1)
    x = merge_data.sample(1000)
    sb.scatterplot(x=col, y='Calories', data=x)
plt.tight_layout()

features = merge_data.select_dtypes(include='float').columns
plt.subplots(figsize=(15, 10))
for i, col in enumerate(features):
    plt.subplot(2, 3, i + 1)
    sb.distplot(merge_data[col])
plt.tight_layout()

plt.figure(figsize=(8, 8))
sb.heatmap(merge_data.corr() > 0.9, annot=True, cbar=False)

# Drop highly correlated features
to_remove = ['Weight', 'Duration']
merge_data.drop(to_remove, axis=1, inplace=True)

plt.show()
