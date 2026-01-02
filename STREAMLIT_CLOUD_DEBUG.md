# 🐛 Streamlit Cloud Deployment - Debugging Guide

## ✅ Pre-Deployment Checklist

Before deploying, verify these files exist:

```bash
✓ requirements.txt       # Python dependencies
✓ packages.txt          # System dependencies (CRITICAL for osmnx)
✓ .python-version       # Python version specification
✓ streamlit_run.py      # Main app file
✓ .streamlit/config.toml # Streamlit config
```

---

## 🔍 Common Deployment Issues & Solutions

### Issue 1: "No module named 'osmnx'" or GDAL errors

**Cause:** System dependencies not installed

**Solution:**
1. Verify `packages.txt` exists with these exact lines:
```
gdal-bin
libgdal-dev
libspatialindex-dev
python3-rtree
```

2. Check deployment logs for "apt-get install" commands
3. Wait for system packages to install BEFORE Python packages

---

### Issue 2: Build timeout or hangs

**Cause:** Large dependencies taking too long

**Solution:**
1. Ensure you're using specific versions (not ranges) in `requirements.txt`
2. Streamlit Cloud has 10-minute build limit
3. Consider pre-generating graph data and committing it:
   ```bash
   # Run locally
   python load_map_bachkhoa.py
   
   # Add exception to .gitignore
   echo "!data/bachkhoa_*.pkl" >> .gitignore
   
   # Commit the data
   git add data/bachkhoa_*.pkl
   git commit -m "Add pre-generated graph data"
   git push
   ```

---

### Issue 3: Memory errors during runtime

**Cause:** Graph download/building exceeds memory limit (1GB free tier)

**Solution:**
1. **RECOMMENDED:** Upload pre-generated graph files (see Issue 2)
2. Use smaller map area (reduce bbox in config.py)
3. Upgrade to Streamlit Cloud paid tier (more memory)

---

### Issue 4: Python version mismatch

**Cause:** Wrong Python version on cloud

**Solution:**
1. Verify `.python-version` exists with `3.9.18`
2. Streamlit Cloud supports Python 3.9-3.11
3. Check deployment logs for Python version

---

### Issue 5: App starts but crashes on "Load Graph"

**Cause:** Network timeout downloading OSM data or memory limit

**Solution:**
**Option A: Upload Pre-generated Data (BEST)**
```bash
# 1. Generate locally
python load_map_bachkhoa.py

# 2. Add to git
git add -f data/bachkhoa_*.pkl

# 3. Commit and push
git commit -m "Add graph data"
git push
```

**Option B: Use smaller area**
Edit `config.py`:
```python
BACHKHOA_BBOX = {
    'north': 21.0080,  # Reduced from 21.0110
    'south': 21.0040,  # Increased from 21.0020
    'east': 105.8480,  # Reduced from 105.8530
    'west': 105.8440,  # Increased from 105.8400
}
```

---

## 🎯 Recommended Deployment Strategy

### Step 1: Prepare Graph Data (Locally)

```bash
cd Project1_NguyenBinhAnh

# Generate graph
python load_map_bachkhoa.py

# Verify files created
ls data/bachkhoa_*.pkl
```

### Step 2: Commit Graph Data

```bash
# Allow .pkl files in git
git add -f data/bachkhoa_Adj.pkl
git add -f data/bachkhoa_Nodes.pkl
git add -f data/bachkhoa_Edges.pkl
git add -f data/bachkhoa_Graph.pkl

# Commit
git commit -m "Add pre-generated graph data for Streamlit Cloud"

# Push
git push origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. New app
3. Repository: your-username/your-repo
4. Branch: main
5. Main file path: `Project1_NguyenBinhAnh/streamlit_run.py`
6. Click **Deploy**

### Step 4: Monitor Deployment Logs

Watch for:
- ✅ "Installing system packages" (packages.txt)
- ✅ "Successfully installed osmnx-1.6.0"
- ✅ "You can now view your Streamlit app"

---

## 📋 Deployment Logs - What to Look For

### ✅ GOOD - Successful Deployment
```
[apt-get] Installing gdal-bin libgdal-dev...
[pip] Successfully installed osmnx-1.6.0 geopandas-0.14.0...
[streamlit] You can now view your Streamlit app in your browser.
```

### ❌ BAD - Failed Deployment
```
ModuleNotFoundError: No module named 'osmnx'
→ Check packages.txt exists

Building wheel for fiona... FAILED
→ GDAL dependencies missing

Killed (signal 9)
→ Out of memory (upload graph data)

Timeout: Build exceeded 10 minutes
→ Upload graph data or use pinned versions
```

---

## 🔧 Quick Fixes

### Fix 1: Force Rebuild
```
Streamlit Cloud Dashboard → ⋮ → Reboot app
```

### Fix 2: Clear Cache
```
Streamlit Cloud Dashboard → ⋮ → Clear cache → Reboot
```

### Fix 3: Check Logs
```
Streamlit Cloud Dashboard → Manage app → View logs
```

---

## 📊 File Size Considerations

Check your graph file sizes:
```bash
ls -lh data/bachkhoa_*.pkl
```

Typical sizes:
- bachkhoa_Adj.pkl: 5-20 MB
- bachkhoa_Nodes.pkl: 2-10 MB
- bachkhoa_Edges.pkl: 5-20 MB
- bachkhoa_Graph.pkl: 30-80 MB

**Total:** 50-130 MB (acceptable for GitHub)

GitHub file limit: 100 MB per file
If bachkhoa_Graph.pkl > 100MB, don't commit it (others can be committed)

---

## 🎯 Final Deployment Command Summary

```bash
# ONE-TIME SETUP
python load_map_bachkhoa.py                    # Generate data
git add -f data/bachkhoa_*.pkl                 # Add to git
git commit -m "Add graph data"                 # Commit
git push origin main                           # Push

# Then deploy on share.streamlit.io
```

---

## 💡 Pro Tips

1. **Always commit graph data** for Streamlit Cloud (avoids memory/timeout issues)
2. **Use pinned versions** in requirements.txt (faster builds)
3. **Check logs first** - most issues are visible in deployment logs
4. **Test locally first** - ensure `streamlit run streamlit_run.py` works
5. **Keep packages.txt** - essential for geospatial libraries

---

## 🆘 Still Not Working?

### Debug Steps:
1. Check deployment logs (most issues show up there)
2. Verify all 5 required files exist
3. Try deploying a minimal test app first
4. Check GitHub repo - ensure files are pushed
5. Verify Python version is 3.9.18

### Get Help:
- Streamlit Community Forum: https://discuss.streamlit.io/
- Include: error logs, requirements.txt, packages.txt content

---

## ✅ Success Indicators

You'll know it worked when:
- ✅ App URL loads without errors
- ✅ Graph loads instantly (if you uploaded data)
- ✅ Can find paths between locations
- ✅ Map visualization displays correctly

---

**Need more help?** Post your deployment logs and I'll help debug! 🚀

