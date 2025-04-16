import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from sklearn.svm import SVC
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor

import warnings
warnings.filterwarnings('ignore')

df1 = pd.read_csv('exercise.csv')
df2 = pd.read_csv('calories.csv')


#print(df1.head()) 
#print(df2.head()) 
#df1.describe()
#df2.describe()

merge_data = pd.merge(df1, df2, how='outer') 
merge_data.replace({'male': 0, 'female': 1},inplace=True)
print(merge_data) 

features = merge_data.drop(['User_ID', 'Calories'], axis=1)
target = merge_data['Calories'].values

X_train, X_val,\
    Y_train, Y_val = train_test_split(features, target,
                                      test_size=0.1,
                                      random_state=22)
X_train.shape, X_val.shape

# Normalizing the features for stable and fast training.
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)


from sklearn.metrics import mean_absolute_error as mae
models = [LinearRegression(), XGBRegressor(),
          Lasso(), RandomForestRegressor(), Ridge()]

for i in range(5):
    models[i].fit(X_train, Y_train)

    print(f'{models[i]} : ')

    train_preds = models[i].predict(X_train)
    print('Training Error : ', mae(Y_train, train_preds))

    val_preds = models[i].predict(X_val)
    print('Validation Error : ', mae(Y_val, val_preds))
    print()
    
for model in models:
    model.fit(X_train, Y_train)

    print(f'{model.__class__.__name__} : ') #Use class name to get the name of the model.

    train_preds = model.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(Y_train, train_preds)) #Calculate RMSE
    print('Training RMSE : ', train_rmse)

    val_preds = model.predict(X_val)
    val_rmse = np.sqrt(mean_squared_error(Y_val, val_preds)) #Calculate RMSE
    print('Validation RMSE : ', val_rmse)
    print()    



for model in models:
    model.fit(X_train, Y_train)

    print(f'{model.__class__.__name__} : ')

    train_preds = model.predict(X_train)
    train_r2 = r2_score(Y_train, train_preds) #Calculate R-squared for training
    print('Training R-squared : ', train_r2)

    val_preds = model.predict(X_val)
    val_r2 = r2_score(Y_val, val_preds) #Calculate R-squared for validation
    print('Validation R-squared : ', val_r2)
    print()




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
sb.heatmap(merge_data.corr() > 0.9,
           annot=True,
           cbar=False)

to_remove = ['Weight', 'Duration']
merge_data.drop(to_remove, axis=1, inplace=True)

plt.show()


