from collections import deque

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
