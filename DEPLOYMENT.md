# 🚀 Streamlit Cloud Deployment Guide

## Deploying to Streamlit Cloud

This guide will help you deploy the Bách Khoa Pathfinding app to **Streamlit Cloud** (https://share.streamlit.io/deploy).

---

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository (public or private)
2. **Streamlit Cloud Account**: Sign up at https://share.streamlit.io
3. **Required Files**: Ensure these files are in your repository:
   - ✅ `streamlit_run.py` (main app file)
   - ✅ `requirements.txt` (Python dependencies)
   - ✅ `packages.txt` (System dependencies - **REQUIRED for osmnx**)
   - ✅ `.streamlit/config.toml` (Streamlit configuration)

---

## 🔧 Required Files Explanation

### 1. `packages.txt` (System Dependencies)
```
gdal-bin
libgdal-dev
libspatialindex-dev
python3-rtree
```
**Why needed?** OSMnx requires GDAL (Geospatial Data Abstraction Library) and spatial indexing libraries that aren't available by default on Streamlit Cloud.

### 2. `requirements.txt` (Python Dependencies)
Uses flexible version ranges (e.g., `>=1.6.0,<2.0.0`) instead of pinned versions to ensure compatibility with Streamlit Cloud's environment.

### 3. `.streamlit/config.toml`
Configures theme and server settings for cloud deployment.

---

## 📦 Deployment Steps

### Step 1: Push to GitHub
```bash
cd Project1_NguyenBinhAnh
git add .
git commit -m "Add deployment configuration for Streamlit Cloud"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/deploy
2. Click **"New app"**
3. Fill in the details:
   - **Repository**: `your-username/your-repo-name`
   - **Branch**: `main` (or your branch name)
   - **Main file path**: `Project1_NguyenBinhAnh/streamlit_run.py`
4. Click **"Deploy!"**

### Step 3: Wait for Build
- First deployment takes 5-10 minutes (building osmnx dependencies)
- Watch the logs for any errors
- System packages from `packages.txt` install first
- Then Python packages from `requirements.txt`

---

## 🐛 Troubleshooting Common Issues

### Issue 1: "No module named 'osmnx'"
**Solution**: Ensure `packages.txt` exists and contains GDAL dependencies.

### Issue 2: GDAL version mismatch
**Solution**: Use version ranges in `requirements.txt` instead of pinned versions:
```
geopandas>=0.12.0
```

### Issue 3: Build timeout
**Solution**: 
- Streamlit Cloud has a build timeout limit
- Reduce dependency versions if needed
- Consider caching graph data (upload pre-generated `.pkl` files)

### Issue 4: Memory issues during first run
**Solution**: 
- Streamlit Cloud has memory limits (1GB free tier)
- Pre-generate and upload `bachkhoa_*.pkl` files to your repo
- Modify `streamlit_run.py` to skip graph building if files exist

---

## 💡 Performance Optimization Tips

### 1. Pre-generate Graph Data (Recommended)
Instead of building the graph on every deployment:

```bash
# Run locally to generate graph files
python load_map_bachkhoa.py
```

This creates:
- `data/bachkhoa_Adj.pkl`
- `data/bachkhoa_Nodes.pkl`
- `data/bachkhoa_Edges.pkl`
- `data/bachkhoa_Graph.pkl`

Then:
1. Add these files to your Git repository
2. Update `.gitignore` to allow `.pkl` files in `data/` folder
3. The app will load existing data instead of downloading from OSM

### 2. Add to `.gitignore` (allow data files)
```gitignore
# Allow pre-generated graph data
!data/bachkhoa_*.pkl
```

### 3. Modify `streamlit_run.py`
The app already checks for existing files before downloading, so no changes needed!

---

## 📊 Expected Build Times

| Stage | Time | Description |
|-------|------|-------------|
| System packages | 2-3 min | Installing GDAL, spatial libraries |
| Python packages | 3-5 min | Installing osmnx, geopandas, etc. |
| First app load | 1-2 min | Loading graph data or downloading OSM |
| **Total first deploy** | **6-10 min** | Complete deployment |
| Subsequent deploys | 1-2 min | Cached dependencies |

---

## 🔒 Environment Variables (Optional)

If you need to configure settings without changing code:

1. In Streamlit Cloud dashboard → **App settings** → **Secrets**
2. Add secrets in TOML format:
```toml
DEBUG = false
VERBOSE = false
```

3. Access in code:
```python
import streamlit as st
DEBUG = st.secrets.get("DEBUG", False)
```

---

## ✅ Deployment Checklist

Before deploying, verify:

- [ ] All files committed to GitHub
- [ ] `packages.txt` exists with GDAL dependencies
- [ ] `requirements.txt` uses version ranges (not pinned)
- [ ] `.streamlit/config.toml` exists
- [ ] Main file path is correct: `Project1_NguyenBinhAnh/streamlit_run.py`
- [ ] (Optional) Pre-generated `.pkl` files uploaded for faster loading

---

## 🌐 After Deployment

Once deployed, your app will be available at:
```
https://share.streamlit.io/[username]/[repo]/[branch]/Project1_NguyenBinhAnh/streamlit_run.py
```

Or use the custom URL provided by Streamlit Cloud.

---

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [OSMnx Documentation](https://osmnx.readthedocs.io/)
- [Handling Dependencies](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/app-dependencies)

---

## 🆘 Still Having Issues?

Check the deployment logs in Streamlit Cloud dashboard for specific error messages. Common fixes:
1. Ensure all imports have corresponding packages in `requirements.txt`
2. Verify file paths are relative (not absolute)
3. Check that data directory is created automatically (uses `os.makedirs`)

Good luck with your deployment! 🚀

