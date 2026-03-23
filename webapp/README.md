# Model Explorer (Flask)

This small Flask app provides a quick UI to:

- List result artifacts in `exports/results`
- Display final performance metrics (if `Final_Model_Performance.csv` exists)
- Upload a CSV and run predictions using exported models + scaler

Files created
- `app.py` – the Flask application
- `templates/index.html` – the UI template
- `requirements.txt` – Python dependencies

How to run locally (Windows / PowerShell)

1. Create and activate a virtualenv (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r webapp\requirements.txt
```

3. Start the app:

```powershell
$Env:FLASK_APP = "webapp\\app.py"
python -m flask run --host=0.0.0.0 --port=5000
```

4. Open http://127.0.0.1:5000 in your browser.

Notes
- The app expects `exports/models` and `exports/preprocessors` to contain the exported models and scaler (these were created by the notebook).
- If you want a single-file self-contained UI instead, I can also create a Streamlit app.
