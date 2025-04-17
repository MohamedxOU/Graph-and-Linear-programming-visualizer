from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt

class LPMenu(QWidget):
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
        
        # Simplex Method (with navigation)
        self.btn_simplex = QPushButton("Simplex Method")
        self.btn_simplex.clicked.connect(self.go_to_simplex)
        self.btn_simplex.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_simplex)

        # Ellipsoid Method (placeholder)
        self.btn_ellipsoid = QPushButton("Ellipsoid Method")
        self.btn_ellipsoid.setObjectName("algorithmButton")
        self.btn_ellipsoid.setEnabled(False)
        button_layout.addWidget(self.btn_ellipsoid)

        # Interior-Point Method (placeholder)
        self.btn_interior = QPushButton("Interior-Point Method")
        self.btn_interior.setObjectName("algorithmButton")
        self.btn_interior.setEnabled(False)
        button_layout.addWidget(self.btn_interior)

        # Column Generation (placeholder)
        self.btn_column = QPushButton("Column Generation")
        self.btn_column.setObjectName("algorithmButton")
        self.btn_column.setEnabled(False)
        button_layout.addWidget(self.btn_column)
        
        # Add spacers
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
            #algorithmButton:disabled {
                background-color: #4C566A;
                color: #D8DEE9;
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

    def go_to_simplex(self):
        try:
            from ui.simplex_page import SimplexPage
            simplex_page = SimplexPage(self.stack)
            self.stack.addWidget(simplex_page)
            self.stack.setCurrentWidget(simplex_page)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to load Simplex page: {str(e)}")

    def go_back(self):
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "HomePage":
                self.stack.setCurrentWidget(widget)
                break