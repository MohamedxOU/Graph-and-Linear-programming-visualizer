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
        
    def go_back(self):
        # Find and switch to the home page in the stack
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "HomePage":  # Adjust if your home page has a different class name
                self.stack.setCurrentWidget(widget)
                break