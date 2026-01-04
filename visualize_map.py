# visualize_map.py
import pickle
import os
from typing import List, Dict, Optional, Tuple

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

from point import Point

def plot_route_with_osmnx(G, route: List[int], filepath: Optional[str] = None):
    """Plot route using osmnx's built-in plotting."""
    fig, ax = ox.plot_graph_route(G, route, 
                                   route_color='red',
                                   route_linewidth=3,
                                   node_size=0,
                                   show=False, 
                                   close=False)
    
    if filepath:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def plot_route_simple(nodes: Dict[int, Point], 
                      edges: List[Tuple[int,int,float]],
                      route: List[int], 
                      filepath: Optional[str] = None):
    """Fallback: plot route using networkx + matplotlib."""
    G = nx.DiGraph()
    for nid, p in nodes.items():
        G.add_node(nid, x=p.lon, y=p.lat)
    for u, v, w in edges:
        if u in nodes and v in nodes:
            G.add_edge(u, v)
    
    pos = {n: (nodes[n].lon, nodes[n].lat) for n in G.nodes()}
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    nx.draw_networkx_edges(G, pos=pos, ax=ax, 
                           edge_color='gray', 
                           width=0.5, 
                           alpha=0.3,
                           arrows=False)
    
    nx.draw_networkx_nodes(G, pos=pos, ax=ax,
                           node_size=8, 
                           node_color='lightblue',
                           alpha=0.6)
    
    if route and len(route) >= 2:
        route_edges = list(zip(route[:-1], route[1:]))
        nx.draw_networkx_edges(G, pos=pos, ax=ax,
                               edgelist=route_edges, 
                               edge_color='red', 
                               width=3.0,
                               arrows=False)
        
        nx.draw_networkx_nodes(G, pos=pos, ax=ax,
                               nodelist=route, 
                               node_size=50, 
                               node_color='red')
        
        nx.draw_networkx_nodes(G, pos=pos, ax=ax,
                               nodelist=[route[0]], 
                               node_size=150, 
                               node_color='green',
                               node_shape='s')
        
        nx.draw_networkx_nodes(G, pos=pos, ax=ax,
                               nodelist=[route[-1]], 
                               node_size=150, 
                               node_color='blue',
                               node_shape='^')
    
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    
    if filepath:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def plot_route_with_graph_or_simple(graph_path: str,
                                    nodes_path: str,
                                    edges_path: str,
                                    route: List[int],
                                    save_png: Optional[str] = None):
    """Main visualization function. Try osmnx first, fall back to networkx."""
    if not route or len(route) < 2:
        return
    
    if os.path.exists(graph_path):
        try:
            with open(graph_path, 'rb') as f:
                G = pickle.load(f)
            plot_route_with_osmnx(G, route, filepath=save_png)
            return
        except:
            pass
    
    with open(nodes_path, 'rb') as f:
        nodes = pickle.load(f)
    with open(edges_path, 'rb') as f:
        edges = pickle.load(f)
    
    plot_route_simple(nodes, edges, route, filepath=save_png)