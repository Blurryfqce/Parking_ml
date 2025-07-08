# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# import joblib

# # Load and prepare data
# df = pd.read_csv('backend/Dataset.csv')
# df['ds'] = pd.to_datetime(df['Datetime'])
# df['y'] = df['Occupancy']

# df['hour'] = df['ds'].dt.hour
# df['day'] = df['ds'].dt.day
# df['dayofweek'] = df['ds'].dt.dayofweek
# df['month'] = df['ds'].dt.month

# df.dropna(inplace=True)

# X = df[['hour', 'day', 'dayofweek', 'month']]
# y = df['y']

# # Train model
# rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
# rf_model.fit(X, y)

# # Save model
# joblib.dump(rf_model, 'backend/rf_parking_model2.pkl')
# print("✅ Model trained and saved successfully!")


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_model():
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    import joblib

    # Load dataset
    df = pd.read_csv('backend/Dataset.csv')

    # Rename columns to match expected names
    df.rename(columns={'Datetime': 'ds', 'Occupancy': 'y'}, inplace=True)

    # Convert to datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # Feature engineering
    df['hour'] = df['ds'].dt.hour
    df['day'] = df['ds'].dt.day
    df['dayofweek'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month

    X = df[['hour', 'day', 'dayofweek', 'month']]
    y = df['y']

    # Train model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)

    # Save model
    joblib.dump(model, 'backend/rf_parking_model2.pkl')
    print("✅ Model trained and saved successfully.")
