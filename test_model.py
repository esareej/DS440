import numpy as np
from joblib import load
from sklearn.metrics import accuracy_score, classification_report

# Assuming functions.py contains necessary functions for processing new data
from functions import extract_frames_from_folders, aggregate_features, predict_with_uncertainty

# Load the trained model
clf = load('deepfake_detection_model.joblib')

# Process the unseen data
# Assuming the functions are adapted to work with the unseen data
unseen_data = extract_frames_from_folders(base_folder='data/unseen')

# Aggregate features for the unseen data
features_unseen, labels_unseen = aggregate_features(unseen_data)

# Predict with the model on unseen data
y_pred_unseen = predict_with_uncertainty(clf, features_unseen)

# Evaluate predictions on unseen data
# Note: This assumes labels_unseen are available. If not, adjust accordingly.
unsure_predictions_unseen = [pred for pred in y_pred_unseen if pred == 2]
confident_predictions_unseen = [pred for i, pred in enumerate(y_pred_unseen) if pred != 2]
confident_truth_unseen = [true for i, true in enumerate(labels_unseen) if y_pred_unseen[i] != 2]

print(f"Unsure Predictions on Unseen Data: {len(unsure_predictions_unseen)}")
if len(confident_predictions_unseen) > 0:
    confident_accuracy_unseen = accuracy_score(confident_truth_unseen, confident_predictions_unseen)
    print(f"Confident Accuracy on Unseen Data: {confident_accuracy_unseen:.4f}")
    
    overall_accuracy_unseen = accuracy_score(labels_unseen, [pred if pred != 2 else 0 for pred in y_pred_unseen])
    print(f"Overall Accuracy on Unseen Data (including 'unsure' as incorrect): {overall_accuracy_unseen:.4f}")
    
    print(classification_report(confident_truth_unseen, confident_predictions_unseen))
else:
    print("No confident predictions made on unseen data.")
