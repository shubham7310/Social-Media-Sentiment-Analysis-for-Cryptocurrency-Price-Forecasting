import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib
import argparse
import os

def prepare_features(df):
    """Engineers features for the prediction model."""
    df['feature_post_count'] = df['post_count']
    df['feature_volume'] = df['volume']
    df['feature_last_hour_close'] = df['close'].shift(1)
    df['target_price'] = df['close']
    df = df.dropna()
    return df

def train_and_evaluate_model(filepath):
    """Loads data, trains a model, evaluates it, and saves it."""
    print(f"Loading data from {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    df = pd.read_csv(filepath, index_col='open_time', parse_dates=True)
    df_features = prepare_features(df)
    
    features = ['feature_post_count', 'feature_volume', 'feature_last_hour_close']
    X = df_features[features]
    y = df_features['target_price']
    
    if len(X) < 2:
        print("Not enough data to train a model.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    print(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

    print("Training the Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    print("Evaluating model performance...")
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model Evaluation - Mean Absolute Error (MAE): ${mae:,.2f}")

    model_filename = 'price_prediction_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nSuccessfully trained and saved model to {model_filename}")

def main():
    parser = argparse.ArgumentParser(description="Train a price prediction model.")
    parser.add_argument("filepath", help="Path to the processed CSV file.")
    args = parser.parse_args()
    train_and_evaluate_model(args.filepath)

if __name__ == "__main__":
    main()