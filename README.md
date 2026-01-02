# 🗺️ Bách Khoa Pathfinding System

A web-based pathfinding application that finds optimal routes between locations in Hanoi University of Science and Technology (Bách Khoa) campus using the A* algorithm and real OpenStreetMap data.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ Features

- 🗺️ **Real Map Data** - Uses OpenStreetMap data via OSMnx
- 🎯 **Smart Pathfinding** - A* algorithm for optimal route finding
- 📍 **Multiple Input Methods** - Coordinates, addresses, or quick-select presets
- 📊 **Route Analysis** - Distance calculations, detour ratios, and metrics
- 🎨 **Interactive UI** - Modern Streamlit web interface
- 💾 **Caching** - Pre-generated graph data for fast loading
- 🌐 **Geocoding** - Address-to-coordinate conversion with Nominatim

---

## 🚀 Quick Start

### Option 1: Automatic Setup (Windows)

Simply double-click:
```
run_local.bat
```

### Option 2: Manual Setup

```bash
# 1. Clone or navigate to project directory
cd Project1_NguyenBinhAnh

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\activate
# or on macOS/Linux:
# source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run streamlit_run.py
```

The app will open in your browser at http://localhost:8501

---

## 📋 Requirements

- Python 3.8 or higher
- Internet connection (for first-time map data download)
- 2GB+ RAM
- 500MB+ disk space

---

## 📦 Dependencies

Main libraries:
- **Streamlit** - Web UI framework
- **OSMnx** - OpenStreetMap data extraction
- **NetworkX** - Graph algorithms and data structures
- **GeoPy** - Geocoding services
- **Matplotlib** - Visualization
- **GeoPandas** - Geospatial data processing

See `requirements.txt` for complete list with versions.

---

## 🎯 Usage

### 1. Load Graph Data

On first run:
1. Click **"Load/Build Graph"** in the sidebar
2. Wait 1-2 minutes for map data download
3. Graph files are saved in `data/` folder for future use

### 2. Find a Path

**Method A: Quick Select (Easiest)**
- Choose locations from dropdown menus
- Pre-configured common campus locations

**Method B: Enter Coordinates**
```
Start: 21.0037, 105.8454
Goal: 21.0042, 105.8458
```

**Method C: Enter Address**
```
Start: Thư viện Tạ Quang Bửu
Goal: Nhà C1
```

### 3. View Results

- Path length (number of nodes)
- Route distance (meters)
- Straight-line distance
- Detour ratio
- Interactive map visualization

---

## 📂 Project Structure

```
Project1_NguyenBinhAnh/
├── streamlit_run.py          # Main Streamlit app
├── run_path.py                # CLI alternative
├── AStar.py                   # A* pathfinding algorithm
├── load_map_bachkhoa.py       # Map data loader
├── visualize_map.py           # Route visualization
├── geocode_address.py         # Address geocoding
├── calcDist.py                # Distance calculations
├── point.py                   # Data models
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── packages.txt               # System dependencies (for Streamlit Cloud)
├── run_local.bat              # Windows launcher
├── LOCAL_SETUP.md             # Detailed setup guide
├── .gitignore                 # Git ignore rules
├── data/                      # Generated data (not in git)
│   ├── bachkhoa_Graph.pkl     # OSMnx graph
│   ├── bachkhoa_Nodes.pkl     # Node dictionary
│   ├── bachkhoa_Edges.pkl     # Edge list
│   └── bachkhoa_Adj.pkl       # Adjacency list
└── .streamlit/
    └── config.toml            # Streamlit configuration
```

---

## 🔧 Configuration

Edit `config.py` to customize:

- **Map boundaries** - Change BACHKHOA_BBOX coordinates
- **Common locations** - Add/modify COMMON_LOCATIONS
- **OSM settings** - Adjust download parameters
- **Visualization** - Change colors, sizes, DPI
- **Paths** - Modify data directory location

---

## 🌐 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io/deploy
3. Connect your repository
4. Set main file: `Project1_NguyenBinhAnh/streamlit_run.py`
5. Deploy!

**Note:** `packages.txt` is required for OSMnx on Streamlit Cloud.

See `DEPLOYMENT.md` for detailed instructions.

---

## 🛠️ Development

### Running Tests

```bash
# Run the CLI version for testing
python run_path.py --start "21.0037,105.8454" --goal "21.0042,105.8458"
```

### Regenerate Graph Data

```bash
python load_map_bachkhoa.py
```

### Clear Cache

In Streamlit app:
- Press `C` in terminal
- Or use menu: ☰ → Settings → Clear cache

---

## 📊 Algorithm Details

### A* Pathfinding

- **Heuristic:** Haversine distance (great-circle distance)
- **Cost Function:** Actual road distances from OSM
- **Complexity:** O((V + E) log V) where V = nodes, E = edges
- **Optimality:** Guaranteed optimal path (admissible heuristic)

### Distance Calculation

Uses Haversine formula:
```
d = 2R × arcsin(√[sin²(Δφ/2) + cos(φ₁)cos(φ₂)sin²(Δλ/2)])
```
Where R = Earth radius (6,371 km)

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Port already in use | Use `--server.port 8502` |
| GDAL installation fails | Use `conda install osmnx` |
| Graph download fails | Check internet connection |
| Geocoding not working | Use coordinates instead |

See `LOCAL_SETUP.md` for detailed troubleshooting.

---

## 📚 Documentation

- **Setup Guide**: `LOCAL_SETUP.md`
- **Deployment Guide**: `DEPLOYMENT.md` (if you need it)
- **Configuration**: See `config.py` comments

---

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- **OpenStreetMap** - Map data
- **OSMnx** - Python library by Geoff Boeing
- **Streamlit** - Web framework
- **Hanoi University of Science and Technology** - Campus data

---

## 📞 Support

For issues or questions:
1. Check `LOCAL_SETUP.md` for setup help
2. Review error messages in terminal
3. Verify all dependencies are installed
4. Try regenerating graph data

---

## 🗺️ Map Coverage

**Default Area:** Hanoi University of Science and Technology (Bách Khoa)
- North: 21.0110°
- South: 21.0020°
- East: 105.8530°
- West: 105.8400°

Coverage: ~0.77 km² of campus area

---

## ⚡ Performance

- **First load:** 1-2 minutes (downloads OSM data)
- **Subsequent loads:** <1 second (uses cached data)
- **Pathfinding:** <100ms for typical campus routes
- **Memory usage:** ~200-500MB
- **Graph size:** ~50-100MB (pickled)

---

## 🎓 Educational Value

This project demonstrates:
- Graph algorithms (A*)
- Web application development (Streamlit)
- Geospatial data processing (OSMnx, GeoPandas)
- API integration (Nominatim geocoding)
- Data visualization (Matplotlib)
- Software architecture and design patterns

---

**Made with ❤️ for Bách Khoa students**

---

## 🔗 Useful Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OSMnx Documentation](https://osmnx.readthedocs.io/)
- [A* Algorithm Explanation](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [OpenStreetMap](https://www.openstreetmap.org/)

---

*Version 1.0.0 - January 2026*

