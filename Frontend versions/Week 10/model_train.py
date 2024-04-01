import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

# Assuming functions.py contains necessary functions
from functions import extract_frames_from_folders, aggregate_features

# Extract and aggregate features
data = extract_frames_from_folders(base_folder='data')
features, labels = aggregate_features(data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Initialize and train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate on the training set
train_predictions = clf.predict(X_train)
train_accuracy = accuracy_score(y_train, train_predictions)
print(f"Training Accuracy: {train_accuracy:.4f}")

# Save the model
dump(clf, 'deepfake_detection_model2.joblib')
print("Model saved to deepfake_detection_model2.joblib")
