"""
EV Range Predictor - Model Training Script
==========================================
Run this script to train and save the model:
    python model_training.py

Best model (Linear Regression) is saved as model.pkl
All model comparison results are printed to console.
"""

import warnings
import numpy as np
import pandas as pd
import pickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score

warnings.filterwarnings('ignore')


def load_and_preprocess():
    """Load and preprocess the EV dataset."""
    print("Loading dataset...")
    data = pd.read_csv('evdataset.csv')
    print(f"  Dataset shape: {data.shape}")
    print(f"  Columns: {list(data.columns)}")

    # Encode categorical Drive column
    data.replace({'Drive': {'Rear': 2, 'Front': 0, 'AWD': 1}}, inplace=True)

    # Select relevant features (based on correlation & domain knowledge)
    FEATURES = [
        'Acceleration 0 - 100 km/h', 'Top Speed', 'Total Power', 'Total Torque',
        'Drive', 'Battery Capacity', 'Charge Power', 'Charge Speed',
        'Fastcharge Speed', 'Gross Vehicle Weight (GVWR)',
        'Max. Payload', 'Cargo Volume', 'Width', 'Length'
    ]

    TARGETS = [
        'Electric Range', 'City - Cold Weather', 'Highway - Cold Weather',
        'Combined - Cold Weather', 'City - Mild Weather',
        'Highway - Mild Weather', 'Combined - Mild Weather'
    ]

    X = data[FEATURES].copy()
    y = data[TARGETS].copy()

    # Check for missing values
    print(f"\n  Missing values in features: {X.isna().sum().sum()}")
    print(f"  Missing values in targets:  {y.isna().sum().sum()}")

    return X, y


def train_and_evaluate(X, y):
    """Train multiple models and compare performance."""
    print("\nNormalizing features...")
    X_normalized = preprocessing.normalize(X)

    print("Splitting data (80% train, 20% test, random_state=42)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_normalized, y, test_size=0.2, random_state=42
    )
    print(f"  Train size: {X_train.shape[0]} samples")
    print(f"  Test  size: {X_test.shape[0]} samples")

    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree Regressor': DecisionTreeRegressor(random_state=42),
        'Random Forest Regressor (100 trees)': RandomForestRegressor(
            n_estimators=100, random_state=42
        ),
    }

    results = {}
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)

    best_model = None
    best_mae = float('inf')
    best_name = ''

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        results[name] = {'mae': mae, 'r2': r2, 'model': model}
        print(f"\n  {name}")
        print(f"    MAE : {mae:.4f} km")
        print(f"    R²  : {r2:.4f}")

        if mae < best_mae:
            best_mae = mae
            best_model = model
            best_name = name

    print("\n" + "="*60)
    print(f"BEST MODEL: {best_name}")
    print(f"  MAE = {best_mae:.4f} km")
    print("="*60)

    return best_model, best_name, X_test, y_test


def save_model(model, path='model.pkl'):
    """Serialize model to disk."""
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved to '{path}'")


def print_feature_stats():
    """Print feature statistics for input validation reference."""
    data = pd.read_csv('evdataset.csv')
    data.replace({'Drive': {'Rear': 2, 'Front': 0, 'AWD': 1}}, inplace=True)
    FEATURES = [
        'Acceleration 0 - 100 km/h', 'Top Speed', 'Total Power', 'Total Torque',
        'Drive', 'Battery Capacity', 'Charge Power', 'Charge Speed',
        'Fastcharge Speed', 'Gross Vehicle Weight (GVWR)',
        'Max. Payload', 'Cargo Volume', 'Width', 'Length'
    ]
    print("\nFEATURE STATISTICS (min / max):")
    for col in FEATURES:
        print(f"  {col:40s}: {data[col].min():.1f} / {data[col].max():.1f}")


if __name__ == '__main__':
    X, y = load_and_preprocess()
    best_model, best_name, X_test, y_test = train_and_evaluate(X, y)
    save_model(best_model)
    print_feature_stats()
    print("\nTraining complete. Run `python app.py` to start the web server.")
