# visualize_map.py
import pickle
import os
from typing import List, Dict, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

from point import Point

def plot_route_with_osmnx(G, route: List[int], filepath: Optional[str] = None):
    """Plot route on actual map with OSMnx - shows all streets"""
    fig, ax = ox.plot_graph_route(
        G, route, 
        route_linewidth=6,
        node_size=0,
        bgcolor='white',
        route_color='red',
        route_alpha=0.8,
        orig_dest_size=100,
        show=False, 
        close=False,
        figsize=(12, 12)
    )
    if filepath:
        fig.savefig(filepath, dpi=200, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def plot_route_simple(nodes: Dict[int, Point], edges: List[Tuple[int,int,float]],
                      route: List[int], filepath: Optional[str] = None):
    """Fallback: plot route with NetworkX - shows full network + highlighted route"""
    G = nx.DiGraph()
    for nid, p in nodes.items():
        G.add_node(nid, x=p.lon, y=p.lat)
    for u,v,w in edges:
        if u in nodes and v in nodes:
            G.add_edge(u, v)
    
    pos = {n: (nodes[n].lon, nodes[n].lat) for n in G.nodes()}
    
    fig, ax = plt.subplots(figsize=(14, 14), facecolor='white')
    
    # Draw ALL edges (the road network background)
    nx.draw_networkx_edges(
        G, pos, 
        edge_color='#999999',
        width=0.5,
        alpha=0.4,
        ax=ax
    )
    
    # Draw ALL nodes (small gray dots)
    nx.draw_networkx_nodes(
        G, pos,
        node_size=1,
        node_color='#666666',
        alpha=0.3,
        ax=ax
    )
    
    # Highlight the ROUTE
    if route and len(route) >= 2:
        route_edges = list(zip(route[:-1], route[1:]))
        
        # Draw route edges (thick red line)
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=route_edges,
            edge_color='red',
            width=3.5,
            alpha=0.9,
            ax=ax
        )
        
        # Draw route nodes (red dots)
        nx.draw_networkx_nodes(
            G, pos, 
            nodelist=route,
            node_size=40,
            node_color='red',
            alpha=0.8,
            ax=ax
        )
        
        # Highlight start and end
        if len(route) > 0:
            # Start node (green)
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=[route[0]],
                node_size=150,
                node_color='green',
                node_shape='o',
                alpha=1.0,
                ax=ax
            )
            # End node (blue)
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=[route[-1]],
                node_size=150,
                node_color='blue',
                node_shape='s',
                alpha=1.0,
                ax=ax
            )
    
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    
    if filepath:
        plt.savefig(filepath, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
    else:
        plt.show()

def plot_route_with_graph_or_simple(graph_path: str,
                                    nodes_path: str,
                                    edges_path: str,
                                    route: List[int],
                                    save_png: Optional[str] = None):
    if os.path.exists(graph_path):
        try:
            with open(graph_path, 'rb') as f:
                G = pickle.load(f)
            plot_route_with_osmnx(G, route, filepath=save_png)
            return
        except Exception as e:
            print("Failed to use graph pickle for plotting:", e)
    with open(nodes_path, 'rb') as f:
        nodes = pickle.load(f)
    with open(edges_path, 'rb') as f:
        edges = pickle.load(f)
    plot_route_simple(nodes, edges, route, filepath=save_png)
