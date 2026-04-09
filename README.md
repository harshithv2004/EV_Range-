# EV Range Predictor — B.Tech Final Year Project

A machine learning web application that predicts electric vehicle range
across **7 driving conditions** from 14 technical specifications.

---

## Project Structure

```
ev_project/
│
├── app.py                  # Flask web application (routes, validation, prediction)
├── model_training.py       # Standalone model training script
├── requirements.txt        # Python dependencies
│
├── evdataset.csv           # Dataset: 194 EVs × 27 features
│
├── templates/
│   ├── index.html          # Input form page
│   ├── result.html         # Prediction results page
│   └── error.html          # Error page
│
└── static/
    ├── css/style.css       # Complete stylesheet (dark theme)
    └── js/main.js          # Client-side UX & validation
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model (creates model.pkl)
python model_training.py

# 3. Start the web server
python app.py
# → Open http://localhost:8000
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      USER BROWSER                        │
│   index.html ──POST──> /predict ──renders──> result.html │
└─────────────────────────────────────────────────────────┘
                              │
                      Flask (app.py)
                              │
             ┌────────────────┴────────────────┐
             │          Preprocessing           │
             │   • Server-side input validation │
             │   • Range checks per feature     │
             │   • L2 Normalization (sklearn)   │
             └────────────────┬────────────────┘
                              │
             ┌────────────────┴────────────────┐
             │      Linear Regression Model     │
             │      (loaded from model.pkl)     │
             │   Inputs:  14 features           │
             │   Outputs: 7 range predictions   │
             └────────────────┬────────────────┘
                              │
             ┌────────────────┴────────────────┐
             │          Predictions             │
             │  • Electric Range               │
             │  • City Cold / Mild             │
             │  • Highway Cold / Mild          │
             │  • Combined Cold / Mild         │
             └─────────────────────────────────┘
```

---

## Model Details

| Model                    | MAE (km) | Notes                         |
|--------------------------|----------|-------------------------------|
| **Linear Regression**    | **~8.95**| ✅ Best — deployed             |
| Random Forest Regressor  | ~14.0    | Overfits small dataset        |
| Decision Tree Regressor  | ~14.5    | Higher variance               |

- **Dataset**: 194 EVs, 14 input features, 7 output targets
- **Preprocessing**: L2 normalization (sklearn.preprocessing.normalize)
- **Split**: 80% train / 20% test, random_state=42
- **Multi-output**: Trained as a single multi-output regression model

---

## Input Features

| Feature                     | Unit   | Range          |
|-----------------------------|--------|----------------|
| Acceleration 0–100 km/h     | s      | 2.8 – 19.1     |
| Top Speed                   | km/h   | 125 – 261      |
| Total Power                 | kW     | 40 – 760       |
| Total Torque                | Nm     | 100 – 1600     |
| Drive (FWD=0, AWD=1, RWD=2) | —      | 0, 1, 2        |
| Battery Capacity            | kWh    | 16.7 – 200     |
| Charge Power                | kW     | 2.3 – 22       |
| Charge Speed                | km/h   | 10 – 110       |
| Fastcharge Speed            | km/h   | 0 – 1170       |
| Gross Vehicle Weight (GVWR) | kg     | 1300 – 3500    |
| Max Payload                 | kg     | 200 – 1200     |
| Cargo Volume                | L      | 100 – 1500     |
| Width                       | mm     | 1600 – 2200    |
| Length                      | mm     | 3500 – 5500    |

---

## API Endpoint

A JSON API endpoint is available for programmatic access:

```bash
POST /api/predict
Content-Type: application/json

{
  "Acceleration 0 - 100 km/h": 7.5,
  "Top Speed": 180,
  "Total Power": 250,
  "Total Torque": 450,
  "Drive": 1,
  "Battery Capacity": 82.0,
  "Charge Power": 11.0,
  "Charge Speed": 49,
  "Fastcharge Speed": 700,
  "Gross Vehicle Weight (GVWR)": 2450,
  "Max. Payload": 570,
  "Cargo Volume": 450,
  "Width": 1890,
  "Length": 4600
}
```

Response:
```json
{
  "success": true,
  "predictions": {
    "Electric Range (km)": 412.5,
    "City - Cold Weather (km)": 390.0,
    ...
  }
}
```
