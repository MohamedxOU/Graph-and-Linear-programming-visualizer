from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt

class GraphMenu(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Button layout for algorithm choices
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(15)
        
        self.btn_bfs = QPushButton("BFS Algorithm")
        self.btn_bfs.clicked.connect(self.go_to_bfs)
        self.btn_bfs.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_bfs)

        self.btn_dfs = QPushButton("DFS Algorithm")
        self.btn_dfs.clicked.connect(self.go_to_dfs)
        self.btn_dfs.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_dfs)

        self.btn_coloring = QPushButton("Greedy Coloring Algorithm")
        self.btn_coloring.clicked.connect(self.go_to_coloring)
        self.btn_coloring.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_coloring)
        
        #Welsh-Powell Coloring Algorithm
        self.btn_welsh_powell = QPushButton("Welsh-Powell Coloring Algorithm")
        self.btn_welsh_powell.clicked.connect(self.go_to_welsh_powell)
        self.btn_welsh_powell.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_welsh_powell)
        
        #prim algorithm
        self.btn_prim = QPushButton("Prim's Algorithm")
        self.btn_prim.clicked.connect(self.go_to_prim)  # Assuming this is a placeholder
        self.btn_prim.setObjectName("algorithmButton")  # Added missing styling
        button_layout.addWidget(self.btn_prim)  # Add to button_layout, not undefined 'layout'
        
        #kruskal algorithm
        self.btn_kruskal = QPushButton("Kruskal's Algorithm")
        self.btn_kruskal.clicked.connect(self.go_to_kruskal)
        self.btn_kruskal.setObjectName("algorithmButton")  # Added missing styling
        button_layout.addWidget(self.btn_kruskal)  # Add to button_layout, not undefined 'layout'
        
        #bellman-ford algorithm
        self.btn_bellman_ford = QPushButton("Bellman-Ford Algorithm")
        self.btn_bellman_ford.clicked.connect(self.go_to_bellman_ford)
        self.btn_bellman_ford.setObjectName("algorithmButton")  # Added missing styling
        button_layout.addWidget(self.btn_bellman_ford)  # Add to button_layout, not undefined 'layout'
        
        
        # Dijkstra's Algorithm
        self.btn_dijkstra = QPushButton("Dijkstra's Algorithm")
        self.btn_dijkstra.clicked.connect(self.go_to_dijkstra)
        self.btn_dijkstra.setObjectName("algorithmButton")  # Added missing styling
        button_layout.addWidget(self.btn_dijkstra)  # Add to button_layout, not undefined 'layout'
        
        #ford-fulkerson algorithm
        self.btn_ford_fulkerson = QPushButton("Ford-Fulkerson Algorithm")
        self.btn_ford_fulkerson.clicked.connect(self.go_to_ford_fulkerson)
        self.btn_ford_fulkerson.setObjectName("algorithmButton")  # Added missing styling
        button_layout.addWidget(self.btn_ford_fulkerson)  # Add to button_layout, not undefined 'layout'
        
        # A* Algorithm
        self.btn_astar = QPushButton("A* Algorithm")
        self.btn_astar.clicked.connect(self.go_to_astar)
        self.btn_astar.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_astar)

        
        # Add spacer to center the buttons vertically
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addLayout(button_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Bottom layout for back button
        bottom_layout = QHBoxLayout()
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.btn_back = QPushButton("← Back to Home")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        bottom_layout.addWidget(self.btn_back)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # Apply styling
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
    
    def go_to_astar(self):
        from ui.astar_page import AStarPage
        astar_page = AStarPage(self.stack)
        self.stack.addWidget(astar_page)
        self.stack.setCurrentWidget(astar_page)