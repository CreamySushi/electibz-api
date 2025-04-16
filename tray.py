import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor

import warnings
warnings.filterwarnings('ignore')

df1 = pd.read_csv('exercise.csv')
df2 = pd.read_csv('calories.csv')

merge_data = pd.merge(df1, df2, how='outer') 
merge_data.replace({'male': 0, 'female': 1}, inplace=True)

features = merge_data.drop(['User_ID', 'Calories'], axis=1)
target = merge_data['Calories'].values

X_train, X_val, Y_train, Y_val = train_test_split(features, target, test_size=0.1, random_state=22)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# **Final Tuned Models to Further Reduce Overfitting**
models = [
    LinearRegression(),
    XGBRegressor(n_estimators=150, learning_rate=0.05, max_depth=4, reg_alpha=0.5, reg_lambda=2),
    Lasso(alpha=0.01),
    RandomForestRegressor(n_estimators=80, max_depth=8, max_features='sqrt'),
    Ridge(alpha=1)
]

for model in models:
    model.fit(X_train, Y_train)

    print(f'{model.__class__.__name__} :')

    train_preds = model.predict(X_train)
    val_preds = model.predict(X_val)

    print('Training Error (MAE): ', mae(Y_train, train_preds))
    print('Validation Error (MAE): ', mae(Y_val, val_preds))

    train_rmse = np.sqrt(mean_squared_error(Y_train, train_preds))
    val_rmse = np.sqrt(mean_squared_error(Y_val, val_preds))

    print('Training RMSE:', train_rmse)
    print('Validation RMSE:', val_rmse)

    train_r2 = r2_score(Y_train, train_preds)
    val_r2 = r2_score(Y_val, val_preds)

    print('Training R-squared:', train_r2)
    print('Validation R-squared:', val_r2)
    print()

# Cross-Validation for More Stability
for model in models:
    scores = cross_val_score(model, X_train, Y_train, cv=5, scoring='r2')
    print(f'Cross-validation R^2 for {model.__class__.__name__}: {np.mean(scores):.4f}')
 
