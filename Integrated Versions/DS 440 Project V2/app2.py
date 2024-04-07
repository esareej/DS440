from flask import Flask, request, redirect, url_for, render_template
from matplotlib import pyplot as plt
from sklearn.discriminant_analysis import StandardScaler
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from joblib import load
import matplotlib
matplotlib.use('Agg')

# Ensure your feature extraction methods are correctly imported
from functions import (analyze_and_visualize_texture, analyze_and_visualize_frequency,
                       analyze_lbp_features, analyze_gabor_features, detect_face, aggregate_features,
                       predict_with_uncertainty, extract_face_frames)

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload():
    return render_template('upload.html')

def process_video(video_path):
    # Load the saved model
    clf = load('deepfake_detection_model2.joblib')

    # Extract face frames from the video
    face_frames = extract_face_frames# Ensure your feature extraction methods are correctly imported
from functions import (analyze_and_visualize_texture, analyze_and_visualize_frequency,
                       analyze_lbp_features, analyze_gabor_features, detect_face, aggregate_features,
                       predict_with_uncertainty, extract_face_frames)

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload():
    return render_template('upload.html')

def process_video(video_path):
    # Load the saved model
    clf = load('deepfake_detection_model2.joblib')

    # Extract face frames from the video
    face_frames = extract_face_frames(video_path, max_frames=15)

    # Check if any face frames were extracted
    if not face_frames:
        return "no_face", None

    # Select a specific frame to visualize its features
    selected_frame = face_frames[0]  # Choose the first frame, you can modify this as needed

    # Analyze and visualize features for the selected frame
    analyze_and_visualize_texture(selected_frame, visualize=True)
    plt.savefig('static/texture_features.png')  # Update the file path
    
    analyze_and_visualize_frequency(selected_frame, visualize=True)
    plt.savefig('static/frequency_features.png')  # Update the file path
    
    analyze_lbp_features(selected_frame, visualize=True)
    plt.savefig('static/lbp_features.png')  # Update the file path
    
    analyze_gabor_features(selected_frame, visualize=True)
    plt.savefig('static/gabor_features.png')  # Update the file path

    # Initialize lists to store features
    texture_features = []
    frequency_features = []
    lbp_features = []
    gabor_features = []

    # Analyze and extract features from each face frame
    for frame in face_frames:
        texture_feature = analyze_and_visualize_texture(frame, visualize=False)
        texture_features.append(texture_feature)

        frequency_feature = analyze_and_visualize_frequency(frame, visualize=False)
        frequency_features.append(frequency_feature)

        lbp_feature = analyze_lbp_features(frame, visualize=False)
        lbp_features.append(lbp_feature)

        gabor_feature = analyze_gabor_features(frame, visualize=False)
        gabor_features.append(gabor_feature)

    # Create a data dictionary with the extracted features
    data = {
        'video': [
            {
                'texture_features': texture_features,
                'frequency_features': frequency_features,
                'lbp_features': lbp_features,
                'gabor_features': gabor_features
            }
        ]
    }

    # Aggregate the features
    aggregated_features, _ = aggregate_features(data)

    # Make predictions with uncertainty
    predictions = predict_with_uncertainty(clf, aggregated_features)

    # Determine the final prediction based on the majority
    final_prediction = max(set(predictions), key=predictions.count)

    if final_prediction == 0:
        result = 'fake'
    elif final_prediction == 1:
        result = 'real'
    else:
        result = 'unsure'

    # Calculate confidence
    confidence = clf.predict_proba(aggregated_features).max()
    print(f"Confidence: {confidence}")
    return result, confidence

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Check if the file is present in the request
        if 'file' not in request.files:
            return redirect(url_for('upload'))
        file = request.files['file']
        # Check if the file is selected and has an allowed extension
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(url_for('upload'))
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Process the video and get the result and confidence
        result, confidence = process_video(file_path)
        # Pass the result and confidence to the result template
        return render_template('result.html', result=result, confidence=confidence)
    return render_template('result.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        # Handle form submission logic here
        return redirect(url_for('thank_you'))
    return render_template('contact_us.html')

@app.route('/terms_of_service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':
    app.run(debug=True)(video_path, max_frames=15)

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Check if the file is present in the request
        if 'file' not in request.files:
            return redirect(url_for('upload'))
        file = request.files['file']
        # Check if the file is selected and has an allowed extension
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(url_for('upload'))
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Process the video and get the result and confidence
        result, confidence = process_video(file_path)
        # Pass the result and confidence to the result template
        return render_template('result.html', result=result, confidence=confidence)
    return render_template('result.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        # Handle form submission logic here
        return redirect(url_for('thank_you'))
    return render_template('contact_us.html')

@app.route('/terms_of_service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':
    app.run(debug=True)