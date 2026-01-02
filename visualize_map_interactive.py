# visualize_map_interactive.py
"""Interactive map visualization using Folium"""

import folium
from folium import plugins
import pickle
from typing import List, Dict, Tuple
from point import Point


def create_interactive_map(
    nodes: Dict[int, Point],
    route: List[int],
    start_coords: Tuple[float, float],
    goal_coords: Tuple[float, float],
    route_distance: float,
    straight_distance: float
) -> folium.Map:
    """
    Create an interactive Folium map with the route highlighted.
    
    Args:
        nodes: Dictionary of node_id -> Point
        route: List of node IDs in the path
        start_coords: (lat, lon) of start location
        goal_coords: (lat, lon) of goal location
        route_distance: Total route distance in meters
        straight_distance: Straight-line distance in meters
        
    Returns:
        folium.Map object
    """
    
    # Calculate center point for map
    if route and len(route) > 0:
        lats = [nodes[nid].lat for nid in route]
        lons = [nodes[nid].lon for nid in route]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
    else:
        center_lat = (start_coords[0] + goal_coords[0]) / 2
        center_lon = (start_coords[1] + goal_coords[1]) / 2
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=16,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add alternative tile layers
    folium.TileLayer('CartoDB positron', name='Light Mode').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark Mode').add_to(m)
    
    # Draw the route path
    if route and len(route) > 1:
        route_coords = [[nodes[nid].lat, nodes[nid].lon] for nid in route]
        
        # Main route line (thick red)
        folium.PolyLine(
            route_coords,
            color='red',
            weight=5,
            opacity=0.8,
            popup=f'Route: {route_distance:.0f}m',
            tooltip='Click for route info'
        ).add_to(m)
        
        # Add semi-transparent outline for better visibility
        folium.PolyLine(
            route_coords,
            color='darkred',
            weight=7,
            opacity=0.3
        ).add_to(m)
    
    # Add START marker (green)
    folium.Marker(
        location=[start_coords[0], start_coords[1]],
        popup=folium.Popup(
            f"""<div style='width: 200px'>
            <h4>🚀 Start Location</h4>
            <b>Coordinates:</b><br>
            {start_coords[0]:.6f}, {start_coords[1]:.6f}<br>
            <b>Nearest Node:</b> {route[0] if route else 'N/A'}
            </div>""",
            max_width=250
        ),
        tooltip='Start Point',
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m)
    
    # Add END marker (blue)
    folium.Marker(
        location=[goal_coords[0], goal_coords[1]],
        popup=folium.Popup(
            f"""<div style='width: 200px'>
            <h4>🎯 Goal Location</h4>
            <b>Coordinates:</b><br>
            {goal_coords[0]:.6f}, {goal_coords[1]:.6f}<br>
            <b>Nearest Node:</b> {route[-1] if route else 'N/A'}
            </div>""",
            max_width=250
        ),
        tooltip='Goal Point',
        icon=folium.Icon(color='blue', icon='flag-checkered', prefix='fa')
    ).add_to(m)
    
    # Add waypoint markers every 5 nodes
    if route and len(route) > 10:
        step = max(1, len(route) // 10)
        for i in range(step, len(route) - 1, step):
            nid = route[i]
            node = nodes[nid]
            folium.CircleMarker(
                location=[node.lat, node.lon],
                radius=3,
                color='red',
                fill=True,
                fillColor='red',
                fillOpacity=0.7,
                popup=f'Waypoint {i}/{len(route)}<br>Node: {nid}',
                tooltip=f'Waypoint {i}'
            ).add_to(m)
    
    # Add info box with route statistics
    info_html = f"""
    <div style="position: fixed; 
                top: 10px; 
                right: 10px; 
                width: 280px; 
                background-color: white; 
                border: 2px solid grey; 
                border-radius: 5px;
                z-index: 9999; 
                font-size: 14px;
                padding: 10px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <h4 style="margin-top:0;">📊 Route Statistics</h4>
        <table style="width:100%; font-size:12px;">
            <tr>
                <td><b>🛣️ Route Distance:</b></td>
                <td style="text-align:right;">{route_distance:.0f} m</td>
            </tr>
            <tr>
                <td><b>📏 Straight Line:</b></td>
                <td style="text-align:right;">{straight_distance:.0f} m</td>
            </tr>
            <tr>
                <td><b>📈 Detour Ratio:</b></td>
                <td style="text-align:right;">{"N/A" if straight_distance == 0 else f"{route_distance/straight_distance:.2f}x"}</td>
            </tr>
            <tr>
                <td><b>🔢 Waypoints:</b></td>
                <td style="text-align:right;">{len(route)}</td>
            </tr>
            <tr>
                <td><b>🚶 Est. Walk Time:</b></td>
                <td style="text-align:right;">{int(route_distance / 1.4 / 60)} min</td>
            </tr>
        </table>
    </div>
    """
    m.get_root().html.add_child(folium.Element(info_html))
    
    # Add fullscreen button
    plugins.Fullscreen(
        position='topleft',
        title='Enter fullscreen',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    # Add measure control
    plugins.MeasureControl(
        position='topleft',
        primary_length_unit='meters',
        secondary_length_unit='kilometers',
        primary_area_unit='sqmeters'
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Fit bounds to show entire route
    if route and len(route) > 1:
        bounds = [
            [min(nodes[nid].lat for nid in route), min(nodes[nid].lon for nid in route)],
            [max(nodes[nid].lat for nid in route), max(nodes[nid].lon for nid in route)]
        ]
        m.fit_bounds(bounds, padding=[50, 50])
    
    return m

