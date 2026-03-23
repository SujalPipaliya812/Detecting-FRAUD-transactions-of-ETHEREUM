# 🚀 Flask Deployment Guide - Step by Step

## 📦 Files to Push to GitHub for Flask Deployment

### ✅ **MUST PUSH** (Essential Files):

```
ethereum-fraud-detection/          (Repository root)
│
├── webapp/                         ✅ PUSH ENTIRE FOLDER
│   ├── app.py                     ✅ Flask application
│   ├── requirements.txt           ✅ Dependencies
│   ├── Dockerfile                 ✅ Docker config
│   ├── templates/                 ✅ PUSH FOLDER
│   │   └── index.html            ✅ Web UI
│   └── sample.csv                ✅ Sample data
│
├── exports/                        ✅ PUSH ENTIRE FOLDER
│   ├── models/                    ✅ PUSH ALL .pkl FILES
│   │   ├── LogisticRegression_best.pkl
│   │   ├── SVM_best.pkl
│   │   └── KNN_best.pkl
│   ├── preprocessors/             ✅ PUSH ALL FILES
│   │   ├── scaler.pkl
│   │   ├── feature_names.json
│   │   └── scaler_meta.json
│   └── results/                   ✅ PUSH ALL FILES
│       ├── Final_Model_Performance.csv
│       ├── Model_Performance_Summary.csv
│       ├── Feature_Importance.csv
│       └── *.png (confusion matrices)
│
├── .gitignore                      ✅ Git ignore rules
└── README.md                       ✅ Documentation
```

### ❌ **DO NOT PUSH** (Automatically Excluded by .gitignore):

```
❌ .venv/                          # Virtual environment
❌ venv/                           # Virtual environment
❌ __pycache__/                    # Python cache
❌ webapp/__pycache__/             # Python cache
❌ *.pyc, *.pyo, *.pyd            # Compiled Python
❌ final.ipynb                     # Jupyter notebooks
❌ Untitled2.ipynb                 # Jupyter notebooks
❌ .ipynb_checkpoints/             # Notebook checkpoints
❌ transaction_dataset.csv         # Large dataset (optional)
❌ .vscode/                        # VS Code settings
❌ convert_to_pdf.py               # Utility scripts
❌ Ethereum_Fraud_Detection_Project_Report.md  # Reports (optional)
```

---

## 🔧 Step 1: Test Flask App Locally

```powershell
# Navigate to project
cd "c:\Users\abhi virani\ML"

# Activate virtual environment (if using one)
# .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r webapp\requirements.txt

# Run Flask app
cd webapp
python app.py

# Test in browser: http://localhost:5000
```

**Expected**: App runs without errors, UI loads properly.

---

## 📝 Step 2: Prepare for GitHub

### Check Current Files
```powershell
cd "c:\Users\abhi virani\ML"
dir
```

### Verify .gitignore is Working
```powershell
git status
# Should NOT show .venv/, __pycache__/, *.ipynb
```

---

## 🎯 Step 3: Git Commands to Push

```powershell
# Navigate to project root
cd "c:\Users\abhi virani\ML"

# Initialize Git (if not already done)
git init

# Add files to staging
git add .gitignore
git add README.md
git add webapp/
git add exports/

# Check what will be committed
git status

# Commit changes
git commit -m "Initial commit: Flask Ethereum Fraud Detection App"

# Create GitHub repo first (see Step 4), then:
git remote add origin https://github.com/AbhiGuru25/ethereum-fraud-detection.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌐 Step 4: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **"+"** → **"New repository"**
3. **Repository name**: `ethereum-fraud-detection`
4. **Description**: "ML-powered Ethereum fraud detection with Flask"
5. **Visibility**: Public (for free deployment)
6. **DO NOT** initialize with README, .gitignore, or license
7. Click **"Create repository"**
8. Copy the repository URL

---

## ☁️ Step 5: Deploy to Cloud (Choose One)

### 🟢 **Option A: Render.com (Recommended - Free & Easy)**

1. **Go to**: [render.com](https://render.com)
2. **Sign up** with GitHub
3. **Click**: "New" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure**:
   ```
   Name: ethereum-fraud-detection
   Region: Oregon (or closest)
   Branch: main
   Root Directory: (leave empty)
   Environment: Python 3
   Build Command: pip install -r webapp/requirements.txt
   Start Command: cd webapp && python app.py
   ```
6. **Advanced Settings**:
   ```
   Environment Variables:
   - PYTHON_VERSION: 3.11
   - PORT: 5000
   ```
7. **Click**: "Create Web Service"
8. **Wait 5-10 minutes** for deployment
9. **Your URL**: `https://ethereum-fraud-detection.onrender.com`

---

### 🔵 **Option B: Railway.app (Fast & Automatic)**

1. **Go to**: [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **Click**: "New Project" → "Deploy from GitHub repo"
4. **Select**: Your repository
5. Railway auto-detects Flask and deploys
6. **Done!** URL provided automatically

---

### 🟠 **Option C: Heroku**

1. **Install Heroku CLI**: [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Procfile** in root directory:
```powershell
echo "web: cd webapp && gunicorn app:app" > Procfile
```

3. **Add gunicorn** to requirements:
```powershell
echo "gunicorn" >> webapp/requirements.txt
```

4. **Deploy**:
```powershell
heroku login
heroku create ethereum-fraud-detection
git push heroku main
heroku open
```

---

### 🟣 **Option D: PythonAnywhere (Free Tier)**

1. **Sign up**: [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload** code via Files or Git
3. **Create Web App**:
   - Python version: 3.10
   - Framework: Flask
   - Source code: `/home/yourusername/ethereum-fraud-detection/webapp/app.py`
4. **Configure**:
   - WSGI file: Point to `webapp/app.py`
   - Static files: `/static/` → `/webapp/static/`
5. **Reload** web app

---

## 🐳 Step 6: Docker Deployment (Optional)

### Build Image
```powershell
cd "c:\Users\abhi virani\ML"
docker build -t ethereum-fraud-detection ./webapp
```

### Run Container
```powershell
docker run -p 5000:5000 ethereum-fraud-detection
```

### Deploy to Docker Hub
```powershell
docker login
docker tag ethereum-fraud-detection YOUR_USERNAME/ethereum-fraud-detection
docker push YOUR_USERNAME/ethereum-fraud-detection
```

---

## ✅ Deployment Checklist

Before pushing to GitHub:

- [ ] Flask app runs locally without errors
- [ ] `webapp/requirements.txt` has all dependencies
- [ ] `exports/models/` contains 3 `.pkl` files
- [ ] `exports/preprocessors/` has scaler and JSON files
- [ ] `.gitignore` excludes virtual environments and cache
- [ ] `README.md` is complete with instructions
- [ ] Tested predictions with sample data
- [ ] UI loads properly in browser

---

## 🐛 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError" after deployment
**Solution**: Add missing package to `webapp/requirements.txt`

### Issue 2: Models not loading
**Solution**: Verify `exports/` folder structure:
```
exports/
├── models/
│   ├── LogisticRegression_best.pkl
│   ├── SVM_best.pkl
│   └── KNN_best.pkl
├── preprocessors/
│   ├── scaler.pkl
│   ├── feature_names.json
│   └── scaler_meta.json
└── results/
```

### Issue 3: Port binding error
**Solution**: Most platforms use environment variable `PORT`:
```python
# In app.py, change:
app.run(host='0.0.0.0', port=5000)
# To:
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Issue 4: File paths not working
**Solution**: Use relative paths from project root:
```python
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
EXPORT_DIR = BASE_DIR / "exports"
```

### Issue 5: Large files rejected by GitHub
**Solution**: GitHub has 100MB file limit
- Check model file sizes: `dir exports\models /s`
- If > 100MB, use Git LFS:
```powershell
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git commit -m "Add Git LFS"
```

---

## 📊 After Deployment

### Test Your Live App
```bash
curl -X POST https://your-app-url.com/predict \
  -d "TxnCount=150" \
  -d "Balance=1.5" \
  -d "AvgGasUsed=21000" \
  -d "TokenTransfers=10" \
  -d "TotalEthReceived=5.2" \
  -d "TotalEthSent=3.8"
```

### Monitor Logs
- **Render**: Dashboard → Logs tab
- **Railway**: Project → Deployments → Logs
- **Heroku**: `heroku logs --tail`

### Update Deployment
```powershell
# Make changes to code
git add .
git commit -m "Update: description"
git push

# Most platforms auto-redeploy on push!
```

---

## 🎉 Success Indicators

Your deployment is successful when:
- ✅ App URL loads the UI
- ✅ Can enter transaction data
- ✅ Predictions work for all 3 models
- ✅ Confidence bars display correctly
- ✅ No console errors
- ✅ Performance metrics table shows

---

## 🔗 Quick Links

- **Render**: [render.com](https://render.com)
- **Railway**: [railway.app](https://railway.app)
- **Heroku**: [heroku.com](https://heroku.com)
- **PythonAnywhere**: [pythonanywhere.com](https://pythonanywhere.com)

---

**Good luck with your deployment! 🚀**
