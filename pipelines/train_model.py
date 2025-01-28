import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Paths
DATA_PATH = "data/backfilled_data_2025-01-20_to_2025-01-27.csv"  # Adjust the filename
MODEL_PATH = "models/"
os.makedirs(MODEL_PATH, exist_ok=True)

# Load data
def load_data(file_path):
    """
    Load historical data from a CSV file.
    """
    data = pd.read_csv(file_path)
    return data

# Preprocess data
def preprocess_data(df):
    """
    Preprocess the raw data for training.
    """
    # Drop columns that aren't needed for training
    df = df.drop(columns=['forecast_date'], errors='ignore')

    # Encode categorical columns
    label_encoder = LabelEncoder()
    df['dominant_pollutant'] = label_encoder.fit_transform(df['dominant_pollutant'])
    df['pollutant'] = label_encoder.fit_transform(df['pollutant'])
    
    # Convert historical_date to datetime and then to numeric (e.g., days since the earliest date)
    if 'historical_date' in df.columns:
        df['historical_date'] = pd.to_datetime(df['historical_date'])
        df['days_since'] = (df['historical_date'] - df['historical_date'].min()).dt.days
    else:
        print("historical_date column is missing. Skipping related features.")
    
    # Extract features from 'timestamp' if available
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['day_of_year'] = df['timestamp'].dt.dayofyear
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
    else:
        print("Timestamp column is missing. Skipping related features.")

    # Separate features (X) and target (y)
    X = df.drop(columns=['aqi'])  # Replace 'aqi' with your target variable column name
    y = df['aqi']  # Replace 'aqi' with your target variable column name
    
    return X, y

# Train model
def train_model(X_train, y_train):
    """
    Train an XGBoost regression model.
    """
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

# Save model
def save_model(model, metrics, output_path):
    """
    Save the trained model and its metadata.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_file = os.path.join(output_path, f"aqi_model_{timestamp}.joblib")
    
    # Save model
    joblib.dump(model, model_file)
    print(f"Model saved to {model_file}")
    
    # Save metrics
    metrics_file = os.path.join(output_path, f"aqi_model_metrics_{timestamp}.txt")
    with open(metrics_file, "w") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    print(f"Metrics saved to {metrics_file}")

# Main training pipeline
def main():
    # Load and preprocess data
    print("Loading data...")
    data = load_data(DATA_PATH)
    X, y = preprocess_data(data)
    print(f"Feature distribution:\n{X.describe()}")

    
    # Check target variable distribution (debugging)
    print(f"Target variable distribution (AQI):\n{y.describe()}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    print("Training model...")
    model = train_model(X_train, y_train)
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    # Predictions vs Actual values (debugging)
    print(f"Predictions vs Actual values:\n{pd.DataFrame({'y_true': y_test, 'y_pred': y_pred})}")
    
    # Calculate MAE and RMSE manually
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5  # Calculate the square root of MSE

    metrics = {"MAE": mae, "RMSE": rmse}
    print(f"Model evaluation metrics: {metrics}")
    
    # Plot Actual vs Predicted (debugging)
    plt.scatter(y_test, y_pred)
    plt.xlabel('Actual AQI')
    plt.ylabel('Predicted AQI')
    plt.title('Actual vs Predicted AQI')
    plt.show()

if __name__ == "__main__":
    main()
