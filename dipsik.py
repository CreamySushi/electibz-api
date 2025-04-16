# Add feature inspection and residual analysis
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error as mae, mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor

# Load data
df1 = pd.read_csv('exercise.csv')
df2 = pd.read_csv('calories.csv')
merge_data = pd.merge(df1, df2, on='User_ID')  # Explicitly specify the merge key
merge_data['Gender'] = merge_data['Gender'].map({'male': 0, 'female': 1})

# Check features
print("Features:", merge_data.drop(['User_ID', 'Calories'], axis=1).columns.tolist())

# Preprocess
X = merge_data.drop(['User_ID', 'Calories'], axis=1)
y = merge_data['Calories']
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=22)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Models (already well-regularized)
models = [
    LinearRegression(),
    XGBRegressor(n_estimators=150, learning_rate=0.05, max_depth=4, reg_alpha=0.5, reg_lambda=2),
    Lasso(alpha=0.01),
    RandomForestRegressor(n_estimators=80, max_depth=8, max_features='sqrt'),
    Ridge(alpha=1)
]

# Evaluate
for model in models:
    model.fit(X_train_scaled, y_train)
    val_pred = model.predict(X_val_scaled)
    print(f"{model.__class__.__name__} Validation R²: {r2_score(y_val, val_pred):.4f}")

# Residual Analysis for XGBoost (check patterns)
xg = XGBRegressor().fit(X_train_scaled, y_train)
residuals = y_val - xg.predict(X_val_scaled)
plt.scatter(y_val, residuals)
plt.xlabel('Actual Calories')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()