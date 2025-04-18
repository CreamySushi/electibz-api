try:
    from xgboost import XGBRegressor
    print("XGBRegressor is available.")
except ImportError:
    print("XGBRegressor is not available. XGBoost may not be installed correctly.")