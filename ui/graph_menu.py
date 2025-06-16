from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QHBoxLayout, QSpacerItem, QSizePolicy, QLabel)
from PyQt6.QtCore import Qt

class GraphMenu(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        header = QLabel("Les algorithmes de graphes")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setObjectName("headerLabel")
        main_layout.addWidget(header)

        # --- Parcours Section ---
        parcours_label = QLabel("Parcours (Traversal)")
        parcours_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parcours_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        main_layout.addWidget(parcours_label)

        parcours_layout = QHBoxLayout()
        self.btn_bfs = QPushButton("BFS Algorithm")
        self.btn_bfs.clicked.connect(self.go_to_bfs)
        self.btn_bfs.setObjectName("algorithmButton")
        parcours_layout.addWidget(self.btn_bfs)

        self.btn_dfs = QPushButton("DFS Algorithm")
        self.btn_dfs.clicked.connect(self.go_to_dfs)
        self.btn_dfs.setObjectName("algorithmButton")
        parcours_layout.addWidget(self.btn_dfs)
        main_layout.addLayout(parcours_layout)

        # --- Coloring Section ---
        coloring_label = QLabel("Coloration (Coloring)")
        coloring_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        coloring_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        main_layout.addWidget(coloring_label)

        coloring_layout = QHBoxLayout()
        self.btn_coloring = QPushButton("Greedy Coloring")
        self.btn_coloring.clicked.connect(self.go_to_coloring)
        self.btn_coloring.setObjectName("algorithmButton")
        coloring_layout.addWidget(self.btn_coloring)

        self.btn_welsh_powell = QPushButton("Welsh-Powell Coloring")
        self.btn_welsh_powell.clicked.connect(self.go_to_welsh_powell)
        self.btn_welsh_powell.setObjectName("algorithmButton")
        coloring_layout.addWidget(self.btn_welsh_powell)
        main_layout.addLayout(coloring_layout)

        # --- Shortest Path Section ---
        shortest_label = QLabel("Plus court chemin (Shortest Path)")
        shortest_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shortest_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        main_layout.addWidget(shortest_label)

        shortest_layout = QHBoxLayout()
        self.btn_dijkstra = QPushButton("Dijkstra's Algorithm")
        self.btn_dijkstra.clicked.connect(self.go_to_dijkstra)
        self.btn_dijkstra.setObjectName("algorithmButton")
        shortest_layout.addWidget(self.btn_dijkstra)

        self.btn_bellman_ford = QPushButton("Bellman-Ford Algorithm")
        self.btn_bellman_ford.clicked.connect(self.go_to_bellman_ford)
        self.btn_bellman_ford.setObjectName("algorithmButton")
        shortest_layout.addWidget(self.btn_bellman_ford)

       
        main_layout.addLayout(shortest_layout)

        # --- Minimum Spanning Tree Section ---
        mst_label = QLabel("Arbre couvrant minimal (MST)")
        mst_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mst_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        main_layout.addWidget(mst_label)

        mst_layout = QHBoxLayout()
        self.btn_prim = QPushButton("Prim's Algorithm")
        self.btn_prim.clicked.connect(self.go_to_prim)
        self.btn_prim.setObjectName("algorithmButton")
        mst_layout.addWidget(self.btn_prim)

        self.btn_kruskal = QPushButton("Kruskal's Algorithm")
        self.btn_kruskal.clicked.connect(self.go_to_kruskal)
        self.btn_kruskal.setObjectName("algorithmButton")
        mst_layout.addWidget(self.btn_kruskal)
        main_layout.addLayout(mst_layout)

        # --- Flow Section ---
        flow_label = QLabel("Flot maximal (Max Flow)")
        flow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        flow_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        main_layout.addWidget(flow_label)

        flow_layout = QHBoxLayout()
        self.btn_ford_fulkerson = QPushButton("Ford-Fulkerson Algorithm")
        self.btn_ford_fulkerson.clicked.connect(self.go_to_ford_fulkerson)
        self.btn_ford_fulkerson.setObjectName("algorithmButton")
        flow_layout.addWidget(self.btn_ford_fulkerson)
        main_layout.addLayout(flow_layout)

        # Spacer and back button
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        bottom_layout = QHBoxLayout()
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.btn_back = QPushButton("← Back to Home")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        bottom_layout.addWidget(self.btn_back)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Styling (keep your existing style)
        self.setStyleSheet("""
            #algorithmButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                min-width: 200px;
            }
            #algorithmButton:hover {
                background-color: #81A1C1;
            }
            #backButton {
                background-color: #4C566A;
                color: #D8DEE9;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            #backButton:hover {
                background-color: #5E81AC;
            }
        """)

    # ... keep your navigation methods unchanged ...

    def go_to_bfs(self):
        from ui.bfs_page import BFSPage
        bfs_page = BFSPage(self.stack)
        self.stack.addWidget(bfs_page)
        self.stack.setCurrentWidget(bfs_page)
  
    def go_to_dfs(self):
        from ui.dfs_page import DFSPage
        dfs_page = DFSPage(self.stack)
        self.stack.addWidget(dfs_page)
        self.stack.setCurrentWidget(dfs_page)

    def go_to_coloring(self):
        from ui.coloring_page import ColoringPage
        coloring_page = ColoringPage(self.stack)
        self.stack.addWidget(coloring_page)
        self.stack.setCurrentWidget(coloring_page)
        
    def go_to_welsh_powell(self):
        from ui.welsh_powell_page import WelshPowellPage
        welsh_powell_page = WelshPowellPage(self.stack)
        self.stack.addWidget(welsh_powell_page)
        self.stack.setCurrentWidget(welsh_powell_page)
        
    def go_to_prim(self):
        from ui.prim_page import PrimPage
        prim_page = PrimPage(self.stack)
        self.stack.addWidget(prim_page)
        self.stack.setCurrentWidget(prim_page)
        
    def go_to_kruskal(self):
        from ui.kruskal_page import KruskalPage
        kruskal_page = KruskalPage(self.stack)
        self.stack.addWidget(kruskal_page)
        self.stack.setCurrentWidget(kruskal_page)
        
    def go_to_bellman_ford(self):
        from ui.bellman_ford_page import BellmanFordPage
        bellman_ford_page = BellmanFordPage(self.stack)
        self.stack.addWidget(bellman_ford_page)
        self.stack.setCurrentWidget(bellman_ford_page)
        
    def go_to_dijkstra(self):
        from ui.dijkstra_page import DijkstraPage
        dijkstra_page = DijkstraPage(self.stack)
        self.stack.addWidget(dijkstra_page)
        self.stack.setCurrentWidget(dijkstra_page)
        
    def go_back(self):
        """Return to the home page"""
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "HomePage":
                self.stack.setCurrentWidget(widget)
                break
    
    def go_to_ford_fulkerson(self):
        from ui.ford_fulkerson_page import FordFulkersonPage
        ford_fulkerson_page = FordFulkersonPage(self.stack)
        self.stack.addWidget(ford_fulkerson_page)
        self.stack.setCurrentWidget(ford_fulkerson_page)
    
