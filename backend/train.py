import pandas as pd
import numpy as np
import glob
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

# Configuration
DATASET_PATH = "../MachineLearningCSV/MachineLearningCVE/*.csv"
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"
FEATURES_PATH = "selected_features.pkl"
TOP_K_FEATURES = 20

def load_data():
    print("Loading datasets...")
    all_files = glob.glob(DATASET_PATH)
    df_list = []
    for filename in all_files:
        print(f"Reading {filename}")
        df = pd.read_csv(filename, index_col=None, header=0, nrows=100000) # Limit rows for stability
        df_list.append(df)
    
    df = pd.concat(df_list, axis=0, ignore_index=True)
    print(f"Total samples: {df.shape[0]}")
    return df

def preprocess(df):
    print("Preprocessing...")
    # Strip column names
    df.columns = df.columns.str.strip()
    
    # Replace Infinity and NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    # Label Encoding
    le = LabelEncoder()
    df['Label'] = le.fit_transform(df['Label'])
    joblib.dump(le, "label_encoder.pkl")
    
    return df

def select_features(X, y):
    print("Selecting features...")
    # Use a smaller subset for feature selection to save time
    X_sample, _, y_sample, _ = train_test_split(X, y, train_size=0.1, random_state=42, stratify=y)
    
    clf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    clf.fit(X_sample, y_sample)
    
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    top_features = X.columns[indices][:TOP_K_FEATURES].tolist()
    print(f"Top {TOP_K_FEATURES} features: {top_features}")
    
    return top_features

def train():
    df = load_data()
    df = preprocess(df)
    
    X = df.drop(['Label'], axis=1)
    y = df['Label']
    
    # Feature Selection
    selected_features = select_features(X, y)
    joblib.dump(selected_features, FEATURES_PATH)
    
    X = X[selected_features]
    
    # Scaling
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    joblib.dump(scaler, SCALER_PATH)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train
    print("Training model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
