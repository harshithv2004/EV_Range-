from flask import Flask, request, jsonify, render_template
from sklearn import preprocessing
import pickle
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load model once at startup
try:
    model = pickle.load(open('model.pkl', 'rb'))
    logger.info("Model loaded successfully.")
except FileNotFoundError:
    logger.error("model.pkl not found. Please run model_training.py first.")
    model = None

# Feature order must match training data
FEATURE_ORDER = [
    'Acceleration 0 - 100 km/h',
    'Top Speed',
    'Total Power',
    'Total Torque',
    'Drive',
    'Battery Capacity',
    'Charge Power',
    'Charge Speed',
    'Fastcharge Speed',
    'Gross Vehicle Weight (GVWR)',
    'Max. Payload',
    'Cargo Volume',
    'Width',
    'Length'
]

OUTPUT_LABELS = [
    'Electric Range (km)',
    'City - Cold Weather (km)',
    'Highway - Cold Weather (km)',
    'Combined - Cold Weather (km)',
    'City - Mild Weather (km)',
    'Highway - Mild Weather (km)',
    'Combined - Mild Weather (km)'
]

FEATURE_RANGES = {
    'Acceleration 0 - 100 km/h': (2.8, 19.1),
    'Top Speed': (125, 261),
    'Total Power': (40, 760),
    'Total Torque': (100, 1600),
    'Drive': (0, 2),
    'Battery Capacity': (16.7, 200.0),
    'Charge Power': (2.3, 22.0),
    'Charge Speed': (10, 110),
    'Fastcharge Speed': (0, 1170),
    'Gross Vehicle Weight (GVWR)': (1300, 3500),
    'Max. Payload': (200, 1200),
    'Cargo Volume': (100, 1500),
    'Width': (1600, 2200),
    'Length': (3500, 5500)
}


@app.route('/')
def index():
    return render_template('index.html', errors=[], form_data={})


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('error.html', message="Model not loaded. Please contact the administrator."), 500

    try:
        values = []
        errors = []

        for feature in FEATURE_ORDER:
            raw = request.form.get(feature, '').strip()
            if not raw:
                errors.append(f"'{feature}' is required.")
                continue
            try:
                val = float(raw)
            except ValueError:
                errors.append(f"'{feature}' must be a number.")
                continue

            # Range validation
            if feature in FEATURE_RANGES:
                low, high = FEATURE_RANGES[feature]
                if not (low <= val <= high):
                    errors.append(f"'{feature}' should be between {low} and {high}.")

            values.append(val)

        if errors:
            return render_template('index.html', errors=errors, form_data=request.form)

        # Normalize and predict
        features_array = np.array([values])
        normalized = preprocessing.normalize(features_array)
        prediction = model.predict(normalized)
        results = np.round(prediction[0], 1).tolist()

        output = dict(zip(OUTPUT_LABELS, results))

        return render_template('result.html', output=output, form_data=request.form)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return render_template('error.html', message="An unexpected error occurred during prediction."), 500


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint for programmatic access."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        values = [float(data.get(f, 0)) for f in FEATURE_ORDER]
        features_array = np.array([values])
        normalized = preprocessing.normalize(features_array)
        prediction = model.predict(normalized)
        results = np.round(prediction[0], 1).tolist()

        return jsonify({
            'success': True,
            'predictions': dict(zip(OUTPUT_LABELS, results))
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# NEW — works both locally and on Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)