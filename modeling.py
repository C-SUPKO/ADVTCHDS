import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
'''Given year state group and type of cancer we can predict the cancer rate with high accuracy.'''
def rfCancer():
    df = pd.read_csv('data/clean_cdi.csv')

    # Focus  on Cancer and per 100,000
    modeldta = df[(df['topic'] == 'Cancer') & (df['datavalueunit'] == 'per 100,000')].copy()

    # Drop missing 
    modeldta = modeldta.dropna(subset=['datavalue'])

   
    modeldta = modeldta[['yearstart', 'datavalue', 'locationdesc', 'stratification1', 'question']]

    # Step 5: Fill missing fields
    modeldta['stratification1'] = modeldta['stratification1'].fillna('Overall')
    modeldta['locationdesc'] = modeldta['locationdesc'].fillna('Unknown')
    modeldta['question'] = modeldta['question'].fillna('Unknown')

    modeldta = pd.get_dummies(modeldta, columns=['locationdesc', 'stratification1', 'question'], drop_first=True)

    X = modeldta.drop(columns=['datavalue'])
    y = modeldta['datavalue']

    y = np.log1p(y)  #Flatten large nums

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    print(f"Cancer R-squared: {r2:.4f}")
    print(f"Cancer MSE: {mse:.4f}")

rfCancer()
