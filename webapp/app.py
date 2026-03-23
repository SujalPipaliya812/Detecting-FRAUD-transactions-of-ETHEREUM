from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
import json
import os

# Use relative paths that work in deployment
BASE_DIR = Path(__file__).parent.parent
EXPORT_DIR = BASE_DIR / "exports"
MODEL_DIR = EXPORT_DIR / "models"
PREPROC_DIR = EXPORT_DIR / "preprocessors"
RESULT_DIR = EXPORT_DIR / "results"

app = Flask(__name__)
app.secret_key = "replace-with-your-secret"

# Load available models and scaler
MODELS = {}
SCALER = None

print("DEBUG: Starting model loading...")
for model_name in ["SVM", "KNN", "LogisticRegression"]:
    path = MODEL_DIR / f"{model_name}_best.pkl"
    print(f"DEBUG: Checking for model {model_name} at {path}")
    if path.exists():
        try:
            MODELS[model_name] = joblib.load(path)
            print(f"DEBUG: Loaded model: {model_name} from {path}")
        except Exception as e:
            print(f"DEBUG: Failed to load {model_name} at {path}: {e}")
    else:
        print(f"DEBUG: Model file not found for {model_name} at {path}")

print(f"DEBUG: Checking for scaler at {PREPROC_DIR / 'scaler.pkl'}")
if (PREPROC_DIR / "scaler.pkl").exists():
    try:
        SCALER = joblib.load(PREPROC_DIR / "scaler.pkl")
        print("DEBUG: Loaded scaler successfully.")
    except Exception as e:
        print(f"DEBUG: Failed to load scaler: {e}")
else:
    print(f"DEBUG: Scaler file not found at {PREPROC_DIR / 'scaler.pkl'}")


def list_results():
    files = []
    if RESULT_DIR.exists():
        for p in sorted(RESULT_DIR.iterdir()):
            files.append(p.name)
    return files


@app.route("/")
def index():
    files = list_results()
    models = list(MODELS.keys())
    # Try to read performance CSV
    perf = None
    perf_path = RESULT_DIR / "Final_Model_Performance.csv"
    if perf_path.exists():
        try:
            perf = pd.read_csv(perf_path)
            perf = perf.to_html(classes="table table-sm table-striped", index=False)
        except Exception:
            perf = None
    return render_template("index.html", files=files, models=models, perf_table=perf)


@app.route("/results/<path:filename>")
def serve_result(filename):
    return send_from_directory(RESULT_DIR, filename)


@app.route("/predict", methods=["POST"])
def predict():
    # Only accept form fields for prediction
    form_fields = ["TxnCount", "Balance", "AvgGasUsed", "TokenTransfers", "TotalEthReceived", "TotalEthSent"]
    print("DEBUG: /predict called. Form fields:", request.form)
    if all(field in request.form for field in form_fields):
        print("DEBUG: All required form fields present.")
        input_row = {field: float(request.form[field]) for field in form_fields}
        print("DEBUG: Input row:", input_row)
        import pandas as pd
        X = pd.DataFrame([input_row])
        print("DEBUG: Input DataFrame columns:", X.columns.tolist())
        expected_features = None
        feature_json = PREPROC_DIR / "feature_names.json"
        print(f"DEBUG: Checking for feature_names.json at {feature_json}")
        if feature_json.exists():
            try:
                with open(feature_json) as f:
                    expected_features = json.load(f)
                print("DEBUG: Loaded expected features:", expected_features)
            except Exception as e:
                print(f"DEBUG: Failed to load feature_names.json: {e}")
                expected_features = None
        if expected_features is not None:
            for col in expected_features:
                if col not in X.columns:
                    print(f"DEBUG: Adding missing column {col} with value 0")
                    X[col] = 0
            X = X[expected_features]
            print("DEBUG: Reordered DataFrame columns:", X.columns.tolist())
        if SCALER is not None and hasattr(SCALER, 'mean_'):
            print("DEBUG: Scaling input with loaded scaler.")
            X_scaled = SCALER.transform(X.values)
        else:
            print("DEBUG: No scaler loaded or scaler missing mean_. Using raw values.")
            X_scaled = X.values
        print("DEBUG: Input for prediction (shape):", X_scaled.shape)
        results = {}
        for name, mdl in MODELS.items():
            print(f"DEBUG: Running prediction for model {name}")
            try:
                preds = mdl.predict(X_scaled)
                proba = None
                if hasattr(mdl, 'predict_proba'):
                    try:
                        proba = mdl.predict_proba(X_scaled).tolist()
                        print(f"DEBUG: {name} predict_proba output:", proba)
                    except Exception as e:
                        print(f"DEBUG: {name} failed in predict_proba: {e}")
                        proba = None
                results[name] = {'predictions': preds.tolist(), 'probabilities': proba}
                print(f"DEBUG: {name} prediction:", preds.tolist())
            except Exception as e:
                print(f"DEBUG: {name} failed during prediction: {e}")
                results[name] = {'error': str(e)}
        print("DEBUG: Prediction results:", results)
        return render_template('index.html', results=results, files=list_results(), models=list(MODELS.keys()))
    else:
        print("DEBUG: Missing required form fields.")
        flash('Please fill out all required fields.')
        return redirect(url_for('index'))


if __name__ == '__main__':
    # Use PORT from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    # Set debug=False for production
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
