import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_model():
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    import joblib

    # Load dataset
    df = pd.read_csv('data/Dataset.csv')

    df.rename(columns={'Datetime': 'ds', 'Occupancy': 'y'}, inplace=True)

    # Convert to datetime
    df['ds'] = pd.to_datetime(df['ds'])

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
    joblib.dump(model, 'backend/rf_parking_model.pkl2')
    print("Model trained and saved successfully.")

train_model()
