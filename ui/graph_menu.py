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
        
        self.btn_dijkstra = QPushButton("Dijkstra's Algorithm")
        self.btn_dijkstra.clicked.connect(self.go_to_dijkstra)
        self.btn_dijkstra.setObjectName("algorithmButton")  # Added missing styling
        button_layout.addWidget(self.btn_dijkstra)  # Add to button_layout, not undefined 'layout'
        
        
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
    
    def go_to_astar(self):
        from ui.astar_page import AStarPage
        astar_page = AStarPage(self.stack)
        self.stack.addWidget(astar_page)
        self.stack.setCurrentWidget(astar_page)