# 🖥️ Local Setup Guide - Bách Khoa Pathfinding System

Complete guide to run the Streamlit app on your local machine.

---

## 📋 Prerequisites

### Required Software:
- **Python 3.8 or higher** (recommended: Python 3.9-3.11)
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Check your Python version:
```bash
python --version
```
or
```bash
python3 --version
```

---

## 🚀 Quick Start (5 Steps)

### Step 1: Navigate to Project Directory
```bash
cd "d:\OneDrive - Hanoi University of Science and Technology\HUST classes\banh\Project1_NguyenBinhAnh"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages (may take 5-10 minutes).

### Step 4: Run the Streamlit App
```bash
streamlit run streamlit_run.py
```

### Step 5: Open in Browser
The app will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy the URL from terminal and paste it in your browser.

---

## 🔧 Detailed Setup Instructions

### Option A: Using Virtual Environment (Recommended)

**Why use virtual environment?**
- Keeps dependencies isolated from other projects
- Prevents version conflicts
- Easy to clean up

```bash
# 1. Navigate to project folder
cd "Project1_NguyenBinhAnh"

# 2. Create virtual environment named 'venv'
python -m venv venv

# 3. Activate the virtual environment
# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# 4. Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# 5. Install all dependencies
pip install -r requirements.txt

# 6. Run the app
streamlit run streamlit_run.py
```

### Option B: Using Conda (Alternative)

If you prefer Conda:

```bash
# 1. Create conda environment
conda create -n bachkhoa python=3.10

# 2. Activate environment
conda activate bachkhoa

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_run.py
```

### Option C: Global Installation (Not Recommended)

Install directly to your system Python:

```bash
# Install dependencies globally
pip install -r requirements.txt

# Run the app
streamlit run streamlit_run.py
```

⚠️ **Warning**: This may cause conflicts with other projects.

---

## 📦 Troubleshooting Installation Issues

### Issue 1: "python: command not found"

**Solution**: Try `python3` instead:
```bash
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### Issue 2: "Cannot activate virtual environment" (Windows PowerShell)

**Solution**: Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
venv\Scripts\Activate.ps1
```

### Issue 3: GDAL installation fails on Windows

**Solution**: Install OSGeo4W or use conda:
```bash
# Using conda (easier for Windows):
conda install -c conda-forge osmnx geopandas
pip install streamlit geopy
```

### Issue 4: "ModuleNotFoundError" when running

**Solution**: Ensure you're in the correct directory and virtual environment is activated:
```bash
# Check current directory
pwd   # macOS/Linux
cd    # Windows

# Should be in Project1_NguyenBinhAnh folder
# Check if virtual environment is active (should see (venv) in prompt)

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 5: Port 8501 already in use

**Solution**: Use a different port:
```bash
streamlit run streamlit_run.py --server.port 8502
```

Or find and kill the process using port 8501:
```bash
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

---

## 🎯 First Run Setup

### Initial Graph Download

On first run, the app needs to download map data from OpenStreetMap:

1. Click **"Load/Build Graph"** in the sidebar
2. Wait 1-2 minutes for download and processing
3. Graph files will be saved in `data/` folder:
   - `bachkhoa_Graph.pkl` (~50-100 MB)
   - `bachkhoa_Nodes.pkl`
   - `bachkhoa_Edges.pkl`
   - `bachkhoa_Adj.pkl`

**Note**: This only happens once! Next time, it loads from saved files instantly.

---

## 🧪 Testing the App

### Test 1: Using Coordinates
1. Start location: `21.0037, 105.8454`
2. Goal location: `21.0042, 105.8458`
3. Click "Find Optimal Path"

### Test 2: Using Quick Select
1. Start: Select "thư viện tạ quang bửu" from dropdown
2. Goal: Select "nhà c1" from dropdown
3. Click "Find Optimal Path"

### Test 3: Using Address (if geocoding works)
1. Start location: `Thư viện Tạ Quang Bửu`
2. Goal location: `Nhà C1`
3. Click "Find Optimal Path"

---

## ⚙️ Configuration Options

### Change Port
```bash
streamlit run streamlit_run.py --server.port 8080
```

### Change Browser
```bash
# Don't open browser automatically
streamlit run streamlit_run.py --server.headless true

# Then manually open: http://localhost:8501
```

### Enable Debug Mode
```bash
# Set environment variable
# Windows (Command Prompt):
set DEBUG=true
streamlit run streamlit_run.py

# Windows (PowerShell):
$env:DEBUG="true"
streamlit run streamlit_run.py

# macOS/Linux:
DEBUG=true streamlit run streamlit_run.py
```

---

## 🛠️ Development Mode

### Auto-reload on code changes
Streamlit automatically reloads when you save changes to Python files.

### View logs
Check the terminal where you ran `streamlit run` for logs and errors.

### Clear cache
If you encounter issues with cached data:
1. Press `C` in the terminal running Streamlit
2. Or click "Clear cache" in the app menu (☰ → Settings → Clear cache)

---

## 📂 Project Files Overview

```
Project1_NguyenBinhAnh/
├── streamlit_run.py       ← Main app file (run this!)
├── requirements.txt       ← Dependencies list
├── config.py             ← Configuration settings
├── AStar.py              ← Pathfinding algorithm
├── load_map_bachkhoa.py  ← Map data loader
├── visualize_map.py      ← Visualization
├── geocode_address.py    ← Address geocoding
├── calcDist.py           ← Distance calculations
├── point.py              ← Data models
├── data/                 ← Generated data (created on first run)
│   └── bachkhoa_*.pkl    ← Graph files
└── venv/                 ← Virtual environment (you create this)
```

---

## 🔄 Updating Dependencies

If you add new packages:

```bash
# 1. Activate virtual environment
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

# 2. Install new package
pip install package-name

# 3. Update requirements.txt
pip freeze > requirements.txt
```

---

## 🧹 Cleanup & Deactivation

### Stop the Streamlit app:
Press `Ctrl + C` in the terminal

### Deactivate virtual environment:
```bash
deactivate
```

### Remove virtual environment (if needed):
```bash
# Windows:
rmdir /s venv

# macOS/Linux:
rm -rf venv
```

---

## 💡 Performance Tips

### Faster startup:
1. Pre-generate graph data (done automatically on first run)
2. Keep graph files in `data/` folder
3. Use `@st.cache_data` (already implemented)

### Reduce memory usage:
- Close other applications
- Clear browser cache
- Restart Streamlit if it becomes slow

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 2 GB | 4+ GB |
| Disk Space | 500 MB | 1 GB |
| Python | 3.8+ | 3.9-3.11 |
| Internet | Required (first run) | Required |

---

## 🆘 Common Issues & Solutions

### "Streamlit command not found"
```bash
# Make sure virtual environment is activated
# Try with python -m:
python -m streamlit run streamlit_run.py
```

### "Address already in use"
```bash
# Use different port
streamlit run streamlit_run.py --server.port 8502
```

### "Permission denied" (macOS/Linux)
```bash
# Make file executable
chmod +x streamlit_run.py
```

### App shows blank page
1. Check terminal for errors
2. Try different browser
3. Clear browser cache (Ctrl+Shift+Delete)
4. Restart Streamlit

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OSMnx Documentation](https://osmnx.readthedocs.io/)
- [A* Algorithm Explanation](https://en.wikipedia.org/wiki/A*_search_algorithm)

---

## ✅ Quick Reference Commands

```bash
# Setup (one time)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run app (every time)
streamlit run streamlit_run.py

# Stop app
Ctrl + C

# Deactivate environment
deactivate
```

---

## 📞 Need Help?

If you encounter issues not covered here:
1. Check the terminal output for error messages
2. Verify all files are in the correct location
3. Ensure Python version is 3.8 or higher
4. Try reinstalling dependencies: `pip install --force-reinstall -r requirements.txt`

Happy pathfinding! 🗺️✨

