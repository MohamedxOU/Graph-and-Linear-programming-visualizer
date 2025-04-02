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
        couleurs_voisins = {couleurs[voisin] for voisin in graphe[sommet] if voisin in couleurs}
        couleur = 1
        while couleur in couleurs_voisins:
            couleur += 1
        couleurs[sommet] = couleur

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

def reconstruct_path(previous_nodes, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = previous_nodes[current]
    path.append(start)
    return path[::-1]



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
            return reconstruct_path(came_from, end)
            
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

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]