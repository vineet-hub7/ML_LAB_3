import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load models and scalers safely
def load_pickle(file_name):
    try:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return None

# Load all required files
model_tennis = load_pickle('model_tennis.pkl')
model_social = load_pickle('model_social.pkl')
scaler_ss = load_pickle('scaler_ss.pkl')
scaler_mm = load_pickle('scaler_mm.pkl')

@app.route('/')
def index():
    # Serves the beautifully designed frontend
    return render_template('index.html')

@app.route('/api/predict_tennis', methods=['POST'])
def predict_tennis():
    try:
        data = request.json
        if not model_tennis:
            return jsonify({'error': 'Tennis model not available on Server.', 'status': 'Error'}), 500

        # Extract features and convert to int
        outlook = int(data.get('outlook'))
        temp = int(data.get('temp'))
        humidity = int(data.get('humidity'))
        wind = int(data.get('wind'))
        
        # Make prediction: features order ['outlook', 'temp', 'humidity', 'wind']
        features = np.array([[outlook, temp, humidity, wind]])
        prediction = model_tennis.predict(features)[0]
        
        # Decode target: No=0, Yes=1
        result = "Yes, play tennis!" if prediction == 1 else "No, do not play."
        return jsonify({'prediction': result, 'prediction_value': int(prediction), 'status': 'Success'})

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'Error'}), 400


@app.route('/api/predict_social', methods=['POST'])
def predict_social():
    try:
        data = request.json
        if not model_social:
            return jsonify({'error': 'Social Network Ads model not available on Server.', 'status': 'Error'}), 500

        age = float(data.get('age'))
        salary = float(data.get('salary'))
        scaler_choice = data.get('scaler_choice', 'standard')

        features = np.array([[age, salary]])
        
        # Apply chosen scaler
        if scaler_choice == 'minmax':
            if not scaler_mm:
                return jsonify({'error': 'MinMax Scaler not loaded on server.', 'status': 'Error'}), 500
            features_scaled = scaler_mm.transform(features)
        else: # Defaults to standard
            if not scaler_ss:
                return jsonify({'error': 'Standard Scaler not loaded on server.', 'status': 'Error'}), 500
            features_scaled = scaler_ss.transform(features)
            
        prediction = model_social.predict(features_scaled)[0]
        
        # Decode target: Not Purchased=0, Purchased=1
        result = "Purchased" if prediction == 1 else "Not Purchased"
        return jsonify({
            'prediction': result, 
            'prediction_value': int(prediction), 
            'scaler_used': scaler_choice,
            'status': 'Success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'Error'}), 400

if __name__ == '__main__':
    # Optional: use port from env port if deployed on Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
