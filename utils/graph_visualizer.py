import matplotlib.pyplot as plt
import networkx as nx

def afficher_graphe(graph, parcours=None, coloriage=None, titre="", weighted=False):
    G = nx.Graph()
    
    # Add edges with weights if present
    for node, neighbors in graph.items():
        if isinstance(neighbors, dict):  # Weighted graph
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        else:  # Unweighted graph
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    
    # Draw the graph
    if weighted:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    if parcours:
        # Highlight path
        path_edges = list(zip(parcours, parcours[1:]))
        edge_colors = ['red' if edge in path_edges or tuple(reversed(edge)) in path_edges 
                      else 'gray' for edge in G.edges()]
        nx.draw(G, pos, with_labels=True, edge_color=edge_colors, width=2)
    elif coloriage:
        # Color nodes
        colors = [coloriage[node] for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=colors, cmap=plt.cm.tab10)
    else:
        nx.draw(G, pos, with_labels=True)
    
    plt.title(titre)
    plt.show()