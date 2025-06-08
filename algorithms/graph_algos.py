from collections import deque
import heapq

" Algorithme BFS "
"  "
def bfs(graphe, noeud_depart):
    visite = set()
    file = deque([noeud_depart])
    chemin = []

    while file:
        noeud = file.popleft()
        if noeud not in visite:
            visite.add(noeud)
            chemin.append(noeud)
            file.extend(graphe.get(noeud, []))
    
    return chemin



" Algorithme DFS "
"  "
def dfs(graphe, noeud_depart, visite=None):
    if visite is None:
        visite = set()

    visite.add(noeud_depart)
    chemin = [noeud_depart]

    for voisin in graphe.get(noeud_depart, []):
        if voisin not in visite:
            chemin.extend(dfs(graphe, voisin, visite))

    return chemin

" Algorithme Coloration Glouton "
"  "
def coloration_glouton(graphe):
    couleurs = {}

    for sommet in graphe:
        couleurs_voisins = {couleurs[voisin] for voisin in 
                            graphe[sommet] if voisin in couleurs}
        couleur = 1
        while couleur in couleurs_voisins:
            couleur += 1
        couleurs[sommet] = couleur
 
    return couleurs


" Algorithme Welsh-Powell "
"  "

def welsh_powell(graphe):
    # Trier les sommets par degré décroissant
    sommets_tries = sorted(graphe.keys(), key=lambda x: -len(graphe[x]))
    
    couleurs = {}
    couleur_disponible = 1
    
    while sommets_tries:
        # Prendre le premier sommet non coloré
        sommet = sommets_tries.pop(0)
        couleurs[sommet] = couleur_disponible
        
        # Trouver tous les sommets non adjacents au sommet courant
        non_adjacents = []
        for s in sommets_tries:
            if s not in graphe[sommet]:
                non_adjacents.append(s)
        
        # Colorier tous les non adjacents avec la même couleur
        for s in non_adjacents:
            couleurs[s] = couleur_disponible
            sommets_tries.remove(s)
        
        couleur_disponible += 1
    
    return couleurs


def dijkstra(graph, start):
    """Dijkstra's shortest path algorithm"""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous_nodes








def a_star(graph, start, end, heuristic):
    """
    A* pathfinding algorithm
    Args:
        graph: Dict {node: {neighbor: cost}}
        start: Starting node
        end: Target node
        heuristic: Dict {node: estimated_distance_to_end}
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]
    
    open_set_hash = {start}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)
        
        if current == end:
            return reconstruct_path_as(came_from, end)
            
        for neighbor, cost in graph[current].items():
            tentative_g_score = g_score[current] + cost
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    return None  # No path found

def reconstruct_path_as(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]





#prim's algorithm for Minimum Spanning Tree (MST)
def prim(graph, start):
    """Prim's algorithm for Minimum Spanning Tree (MST)"""
    mst = {}
    visited = set([start])
    edges = [
        (weight, start, neighbor)
        for neighbor, weight in graph[start].items()
    ]
    heapq.heapify(edges)
    
    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            if u not in mst:
                mst[u] = {}
            mst[u][v] = weight
            if v not in mst:
                mst[v] = {}
            mst[v][u] = weight
            
            for neighbor, edge_weight in graph[v].items():
                if neighbor not in visited:
                    heapq.heappush(edges, (edge_weight, v, neighbor))
    
    return mst



#kruskal's algorithm for Minimum Spanning Tree (MST)
def kruskal(graph):
    """Kruskal's algorithm for Minimum Spanning Tree (MST)"""
    mst = {}
    parent = {}
    rank = {}
    
    # Initialize disjoint set
    for node in graph:
        parent[node] = node
        rank[node] = 0
    
    # Create list of all edges sorted by weight
    edges = []
    for u in graph:
        for v, weight in graph[u].items():
            edges.append((weight, u, v))
    edges.sort()
    
    # Kruskal's algorithm
    for weight, u, v in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)
        
        if root_u != root_v:
            # Add edge to MST
            if u not in mst:
                mst[u] = {}
            mst[u][v] = weight
            if v not in mst:
                mst[v] = {}
            mst[v][u] = weight
            
            # Union the sets
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            else:
                parent[root_u] = root_v
                if rank[root_u] == rank[root_v]:
                    rank[root_v] += 1
                    
    return mst

def find(parent, node):
    """Find root of node with path compression"""
    if parent[node] != node:
        parent[node] = find(parent, parent[node])
    return parent[node]




def bellman_ford(graph, start):
    """Bellman-Ford algorithm for shortest paths with negative weights"""
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0
    
    # Relax all edges |V| - 1 times
    for _ in range(len(graph) - 1):
        updated = False
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    updated = True
        if not updated:
            break
    
    # Check for negative weight cycles
    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                return None, None  # Negative cycle detected
    
    return distances, predecessors

def reconstruct_path_bf(predecessors, start, end):
    """Reconstruct path from Bellman-Ford predecessors"""
    path = []
    current = end
    while current != start:
        if current is None:
            return []  # No path exists
        path.append(current)
        current = predecessors[current]
    path.append(start)
    return path[::-1]



#ford fulkerson algorithm for maximum flow


def ford_fulkerson(graph, source, sink):
    """Ford-Fulkerson algorithm for maximum flow"""
    # Create residual graph
    residual = {u: {v: weight for v, weight in neighbors.items()} 
               for u, neighbors in graph.items()}
    
    # Add reverse edges with 0 capacity if not present
    for u in list(residual.keys()):
        for v in list(residual[u].keys()):
            if v not in residual:
                residual[v] = {}
            if u not in residual[v]:
                residual[v][u] = 0
    
    parent = {}
    max_flow = 0
    
    # Augment the flow while there is path from source to sink
    while bfs_ff(residual, source, sink, parent):
        # Find minimum residual capacity of the path
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]
        
        # Update residual capacities and reverse edges
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
        
        max_flow += path_flow
    
    # Reconstruct the flow network
    flow_network = {u: {} for u in graph}
    for u in graph:
        for v in graph[u]:
            flow_network[u][v] = graph[u][v] - residual[u][v] if v in residual[u] else 0
    
    return max_flow, flow_network

def bfs_ff(residual, source, sink, parent):
    """BFS to find augmenting path in residual graph"""
    visited = {node: False for node in residual}
    queue = deque()
    queue.append(source)
    visited[source] = True
    
    while queue:
        u = queue.popleft()
        
        for v in residual[u]:
            if not visited[v] and residual[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == sink:
                    return True
                queue.append(v)
    
    return False