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
        
        
        #Standard Simplex Method (with navigation)
        self.btn_standard_simplex = QPushButton("Standard Simplex Method (≤ constraints only)")
        self.btn_standard_simplex.clicked.connect(self.go_to_standard_simplex)
        self.btn_standard_simplex.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_standard_simplex)
        
        # Two-Phase Simplex Method (with navigation)
        self.btn_two_phase_simplex = QPushButton("Two-Phase Simplex Method (Mixed Constraints)")
        self.btn_two_phase_simplex.clicked.connect(self.go_to_two_phase_simplex)
        self.btn_two_phase_simplex.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_two_phase_simplex)
        
        #revised simplex method
        self.btn_revised_simplex = QPushButton("Revised Simplex Method (Standard Form)")
        self.btn_revised_simplex.clicked.connect(self.go_to_revised_simplex)
        self.btn_revised_simplex.setObjectName("algorithmButton")
        button_layout.addWidget(self.btn_revised_simplex)
        
        
        
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

   
    
    def go_to_standard_simplex(self):
        try:
            from ui.standard_simplex_page import StandardSimplexPage
            standard_simplex_page = StandardSimplexPage(self.stack)
            self.stack.addWidget(standard_simplex_page)
            self.stack.setCurrentWidget(standard_simplex_page)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to load Standard Simplex page: {str(e)}")
    
    # go to two phase simplex page
    def go_to_two_phase_simplex(self):
        try:
            from ui.two_phase_simplex_page import TwoPhaseSimplexPage
            two_phase_simplex_page = TwoPhaseSimplexPage(self.stack)
            self.stack.addWidget(two_phase_simplex_page)
            self.stack.setCurrentWidget(two_phase_simplex_page)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to load Two-Phase Simplex page: {str(e)}")
    
    #revised simplex method
    def go_to_revised_simplex(self):
        try:
            from ui.revised_simplex_page import RevisedSimplexPage
            revised_simplex_page = RevisedSimplexPage(self.stack)
            self.stack.addWidget(revised_simplex_page)
            self.stack.setCurrentWidget(revised_simplex_page)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to load Revised Simplex page: {str(e)}")

    def go_back(self):
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "HomePage":
                self.stack.setCurrentWidget(widget)
                break