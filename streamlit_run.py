import streamlit as st
import pickle
import os
import sys
from typing import Optional, Tuple

# Show loading message immediately
st.set_page_config(
    page_title="Bách Khoa Pathfinding",
    page_icon="🗺️",
    layout="wide"
)

# Lazy imports - only import when needed
@st.cache_resource
def lazy_imports():
    """Import heavy modules only once"""
    try:
        from load_map_bachkhoa import build_and_save_graph, DATA_DIR
        from AStar import astar, nearest_node_by_coord
        from visualize_map import plot_route_with_graph_or_simple
        from calcDist import haversine_m
        
        try:
            from geocode_address import get_location_with_fallback, COMMON_LOCATIONS
            geocoding_available = True
        except ImportError:
            get_location_with_fallback = None
            COMMON_LOCATIONS = {}
            geocoding_available = False
        
        return {
            'build_and_save_graph': build_and_save_graph,
            'DATA_DIR': DATA_DIR,
            'astar': astar,
            'nearest_node_by_coord': nearest_node_by_coord,
            'plot_route_with_graph_or_simple': plot_route_with_graph_or_simple,
            'haversine_m': haversine_m,
            'get_location_with_fallback': get_location_with_fallback,
            'COMMON_LOCATIONS': COMMON_LOCATIONS,
            'geocoding_available': geocoding_available
        }
    except Exception as e:
        st.error(f"Error importing modules: {e}")
        return None

# Load modules
modules = lazy_imports()
if modules is None:
    st.stop()

# Extract modules
build_and_save_graph = modules['build_and_save_graph']
DATA_DIR = modules['DATA_DIR']
astar = modules['astar']
nearest_node_by_coord = modules['nearest_node_by_coord']
plot_route_with_graph_or_simple = modules['plot_route_with_graph_or_simple']
haversine_m = modules['haversine_m']
get_location_with_fallback = modules['get_location_with_fallback']
COMMON_LOCATIONS = modules['COMMON_LOCATIONS']
GEOCODING_AVAILABLE = modules['geocoding_available']

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'graph_loaded' not in st.session_state:
    st.session_state.graph_loaded = False
if 'path_result' not in st.session_state:
    st.session_state.path_result = None

@st.cache_data
def load_graph_data(save_prefix: str = "bachkhoa_"):
    """Load graph data with caching"""
    adj_path = os.path.join(DATA_DIR, f"{save_prefix}Adj.pkl")
    nodes_path = os.path.join(DATA_DIR, f"{save_prefix}Nodes.pkl")
    edges_path = os.path.join(DATA_DIR, f"{save_prefix}Edges.pkl")
    graph_path = os.path.join(DATA_DIR, f"{save_prefix}Graph.pkl")
    
    if not all(os.path.exists(p) for p in [adj_path, nodes_path, edges_path, graph_path]):
        return None
    
    with open(adj_path, 'rb') as f:
        adj = pickle.load(f)
    with open(nodes_path, 'rb') as f:
        nodes = pickle.load(f)
    with open(edges_path, 'rb') as f:
        edges = pickle.load(f)
    with open(graph_path, 'rb') as f:
        G = pickle.load(f)
    
    return {
        'adj': adj,
        'nodes': nodes,
        'edges': edges,
        'graph': G,
        'paths': {
            'adj': adj_path,
            'nodes': nodes_path,
            'edges': edges_path,
            'graph': graph_path
        }
    }

def parse_location(location_str: str) -> Tuple[Optional[float], Optional[float]]:
    """Parse location string as coordinates or address"""
    location_str = location_str.strip()
    
    # Try parsing as coordinates
    if ',' in location_str:
        try:
            parts = location_str.split(',')
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return lat, lon
        except ValueError:
            pass
    
    # Try geocoding
    if GEOCODING_AVAILABLE:
        try:
            return get_location_with_fallback(location_str)
        except Exception as e:
            st.error(f"Geocoding failed: {e}")
            return None, None
    
    return None, None

def find_nearest_node(graph_data, lat: float, lon: float) -> Optional[int]:
    """Find nearest node to coordinates"""
    try:
        import osmnx as ox
        G = graph_data['graph']
        return ox.nearest_nodes(G, lon, lat)
    except Exception:
        return nearest_node_by_coord(graph_data['nodes'], lat, lon)

# Main UI
st.markdown('<div class="main-header">🗺️ Bách Khoa Pathfinding System</div>', unsafe_allow_html=True)

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Map settings
    with st.expander("📍 Map Boundaries", expanded=False):
        st.write("Bách Khoa default area:")
        north = st.number_input("North", value=21.0110, format="%.6f")
        south = st.number_input("South", value=21.0020, format="%.6f")
        east = st.number_input("East", value=105.8530, format="%.6f")
        west = st.number_input("West", value=105.8400, format="%.6f")
        save_prefix = st.text_input("Save prefix", value="bachkhoa_")
    
    # Load/Build graph
    st.subheader("📊 Graph Status")
    
    if st.button("🔄 Load/Build Graph", type="primary"):
        with st.spinner("Loading graph data..."):
            try:
                # Try to load existing graph
                graph_data = load_graph_data(save_prefix)
                
                if graph_data is None:
                    st.info("No existing graph found. Building new graph...")
                    build_and_save_graph(north, south, east, west, save_prefix)
                    graph_data = load_graph_data(save_prefix)
                
                st.session_state.graph_data = graph_data
                st.session_state.graph_loaded = True
                st.success("✅ Graph loaded successfully!")
                
                # Show stats
                st.metric("Nodes", len(graph_data['nodes']))
                st.metric("Edges", len(graph_data['edges']))
                
            except Exception as e:
                st.error(f"❌ Error loading graph: {e}")
                st.session_state.graph_loaded = False
    
    if st.session_state.graph_loaded:
        st.success("Graph Ready ✅")
        graph_data = st.session_state.graph_data
        st.metric("Total Nodes", len(graph_data['nodes']))
        st.metric("Total Edges", len(graph_data['edges']))

# Main content
if not st.session_state.graph_loaded:
    st.info("👈 Please load the graph data from the sidebar to begin")
    st.markdown("""
    ### Welcome to Bách Khoa Pathfinding!
    
    This application helps you find the optimal path between two locations in the Bách Khoa area using the A* algorithm.
    
    **Features:**
    - 🗺️ Real map data from OpenStreetMap
    - 🎯 Smart pathfinding with A* algorithm
    - 📍 Support for coordinates and addresses
    - 📊 Distance calculations and route visualization
    
    **To get started:**
    1. Click "Load/Build Graph" in the sidebar
    2. Enter your start and goal locations
    3. Find the optimal path!
    """)
else:
    graph_data = st.session_state.graph_data
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Start Location")
        
        # Quick select for common locations
        if COMMON_LOCATIONS:
            start_preset = st.selectbox(
                "Quick select (Start)",
                ["Custom"] + list(COMMON_LOCATIONS.keys()),
                key="start_preset"
            )
            if start_preset != "Custom":
                coords = COMMON_LOCATIONS[start_preset]
                start_input = f"{coords[0]}, {coords[1]}"
            else:
                start_input = st.text_input(
                    "Start location",
                    placeholder="21.0037, 105.8454 or 'Thư viện Tạ Quang Bửu'",
                    key="start_input"
                )
        else:
            start_input = st.text_input(
                "Start location",
                placeholder="21.0037, 105.8454 or address",
                key="start_input"
            )
    
    with col2:
        st.subheader("🎯 Goal Location")
        
        # Quick select for common locations
        if COMMON_LOCATIONS:
            goal_preset = st.selectbox(
                "Quick select (Goal)",
                ["Custom"] + list(COMMON_LOCATIONS.keys()),
                key="goal_preset"
            )
            if goal_preset != "Custom":
                coords = COMMON_LOCATIONS[goal_preset]
                goal_input = f"{coords[0]}, {coords[1]}"
            else:
                goal_input = st.text_input(
                    "Goal location",
                    placeholder="21.0042, 105.8458 or 'Nhà C1'",
                    key="goal_input"
                )
        else:
            goal_input = st.text_input(
                "Goal location",
                placeholder="21.0042, 105.8458 or address",
                key="goal_input"
            )
    
    # Find path button
    if st.button("🔍 Find Optimal Path", type="primary", use_container_width=True):
        if not start_input or not goal_input:
            st.error("Please enter both start and goal locations")
        else:
            with st.spinner("Finding optimal path..."):
                try:
                    # Parse locations
                    start_lat, start_lon = parse_location(start_input)
                    goal_lat, goal_lon = parse_location(goal_input)
                    
                    if start_lat is None or goal_lat is None:
                        st.error("Failed to parse locations. Please check your input.")
                    else:
                        # Calculate straight-line distance
                        straight_dist = haversine_m(start_lat, start_lon, goal_lat, goal_lon)
                        
                        # Find nearest nodes
                        start_node = find_nearest_node(graph_data, start_lat, start_lon)
                        goal_node = find_nearest_node(graph_data, goal_lat, goal_lon)
                        
                        # Run A*
                        path, cost_m = astar(
                            graph_data['adj'],
                            graph_data['nodes'],
                            start_node,
                            goal_node
                        )
                        
                        if not path:
                            st.error("❌ No path found between these locations")
                        else:
                            # Store results
                            st.session_state.path_result = {
                                'path': path,
                                'cost': cost_m,
                                'straight_dist': straight_dist,
                                'start_coords': (start_lat, start_lon),
                                'goal_coords': (goal_lat, goal_lon),
                                'start_node': start_node,
                                'goal_node': goal_node
                            }
                            
                            st.success("✅ Path found successfully!")
                
                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Display results
    if st.session_state.path_result:
        result = st.session_state.path_result
        
        st.markdown("---")
        st.subheader("📊 Path Analysis")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Path Length", f"{len(result['path'])} nodes")
        with col2:
            st.metric("Route Distance", f"{result['cost']:.1f} m")
        with col3:
            st.metric("Straight Distance", f"{result['straight_dist']:.1f} m")
        with col4:
            detour_ratio = result['cost'] / result['straight_dist']
            st.metric("Detour Ratio", f"{detour_ratio:.2f}x")
        
        # Visualization
        st.subheader("🗺️ Route Visualization")
        
        with st.spinner("Generating map..."):
            try:
                # Create visualization
                output_path = os.path.join(DATA_DIR, "temp_route.png")
                plot_route_with_graph_or_simple(
                    graph_data['paths']['graph'],
                    graph_data['paths']['nodes'],
                    graph_data['paths']['edges'],
                    result['path'],
                    output_path
                )
                
                # Display image
                st.image(output_path, use_container_width=True)
                
                # Download button
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Route Map",
                        data=file,
                        file_name="route_map.png",
                        mime="image/png"
                    )
                
            except Exception as e:
                st.error(f"Visualization error: {e}")
        
        # Path details
        with st.expander("🔍 View Path Details"):
            st.write(f"**Number of waypoints:** {len(result['path'])}")
            st.write(f"**Start node:** {result['start_node']}")
            st.write(f"**Goal node:** {result['goal_node']}")
            
            if st.checkbox("Show all nodes in path"):
                st.write(result['path'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Bách Khoa Pathfinding System | Powered by A* Algorithm & OpenStreetMap</p>
</div>
""", unsafe_allow_html=True)