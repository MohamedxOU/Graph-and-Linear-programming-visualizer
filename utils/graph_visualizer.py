import networkx as nx
import matplotlib.pyplot as plt

def afficher_graphe(graphe, parcours=None, coloriage=None, titre="Graph"):
    G = nx.Graph()

    for noeud, voisins in graphe.items():
        for voisin in voisins:
            G.add_edge(noeud, voisin)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(6, 4))

    if parcours:
        for i, n in enumerate(parcours):
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=2000, font_size=10)
            couleurs = ['blue' if x in parcours[:i+1] else 'lightgray' for x in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=couleurs, edge_color='gray', node_size=2000, font_size=10)
            plt.title(f"{titre} - Step {i+1}/{len(parcours)}")
            plt.pause(0.5)

    elif coloriage:
        couleurs = [coloriage[n] for n in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=couleurs, cmap=plt.cm.Set1, edge_color='gray', node_size=2000, font_size=10)
        plt.title("Graph Coloring")

    plt.show()
