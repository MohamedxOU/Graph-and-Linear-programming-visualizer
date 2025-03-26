from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)  # Add some margin around the edges
        
        # Header section
        header = QLabel("Algorithm Visualizer")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setObjectName("headerLabel")
        main_layout.addWidget(header)
        
        # Add vertical spacer to push content down a bit
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Button layout
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)  # Space between buttons
        button_layout.setContentsMargins(60, 0, 60, 0)  # Left/right margins
        
        self.btn_graph = QPushButton("Graph Algorithms")
        self.btn_graph.clicked.connect(self.go_to_graph_menu)
        self.btn_graph.setObjectName("mainMenuButton")
        button_layout.addWidget(self.btn_graph)

        self.btn_lp = QPushButton("Linear Programming Algorithms")
        self.btn_lp.clicked.connect(self.go_to_lp_menu)
        self.btn_lp.setObjectName("mainMenuButton")
        button_layout.addWidget(self.btn_lp)
        
        main_layout.addLayout(button_layout)
        
        # Add expanding spacer to push everything up
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Footer note
        footer = QLabel("Select an algorithm category to begin")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setObjectName("footerLabel")
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
        
        # Apply styling
        self.setStyleSheet("""
            HomePage {
                background-color: #2E3440;
            }
            
            #headerLabel {
                font-size: 32px;
                font-weight: bold;
                color: #81A1C1;
                padding: 20px;
            }
            
            #mainMenuButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 10px;
                padding: 18px;
                font-size: 18px;
                font-weight: 600;
                min-height: 60px;
            }
            
            #mainMenuButton:hover {
                background-color: #81A1C1;
            }
            
            #mainMenuButton:pressed {
                background-color: #88C0D0;
            }
            
            #footerLabel {
                font-size: 14px;
                color: #D8DEE9;
                font-style: italic;
                padding: 10px;
            }
        """)

    def go_to_graph_menu(self):
        from ui.graph_menu import GraphMenu  # Imported here to prevent circular import
        graph_menu = GraphMenu(self.stack)
        self.stack.addWidget(graph_menu)
        self.stack.setCurrentWidget(graph_menu)

    def go_to_lp_menu(self):
        from ui.lp_menu import LPMenu  # Assuming you'll create this
        lp_menu = LPMenu(self.stack)
        self.stack.addWidget(lp_menu)
        self.stack.setCurrentWidget(lp_menu)