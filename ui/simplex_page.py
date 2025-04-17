import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy,
    QRadioButton
)
from PyQt6.QtCore import Qt
from algorithms.lp_algos.simplex import simplex

class SimplexPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Back button
        back_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to LP Menu")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        back_layout.addWidget(self.btn_back)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Simplex Method for Linear Programming")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        # Input tabs
        self.tabs = QTabWidget()
        
        # Standard form tab
        std_tab = QWidget()
        std_layout = QVBoxLayout()
        
        std_layout.addWidget(QLabel("Objective Function (comma-separated coefficients):"))
        self.entry_objective = QLineEdit("3, 2")
        std_layout.addWidget(self.entry_objective)
        
        std_layout.addWidget(QLabel("Constraints (one per line, format: 'a1,a2,... <= b'):"))
        self.entry_constraints = QTextEdit()
        self.entry_constraints.setPlainText(
            "1, 1 <= 4\n"
            "2, 1 <= 5\n"
            "-1, 2 <= 2"
        )
        std_layout.addWidget(self.entry_constraints)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Optimization:"))
        self.radio_max = QRadioButton("Maximize")
        self.radio_max.setChecked(True)
        self.radio_min = QRadioButton("Minimize")
        type_layout.addWidget(self.radio_max)
        type_layout.addWidget(self.radio_min)
        type_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        std_layout.addLayout(type_layout)
        
        std_tab.setLayout(std_layout)
        self.tabs.addTab(std_tab, "Standard Form")

        # Tableau tab
        tableau_tab = QWidget()
        tableau_layout = QVBoxLayout()
        tableau_layout.addWidget(QLabel("Enter initial tableau (one row per line):"))
        
        self.tableau_table = QTableWidget()
        self.tableau_table.setColumnCount(4)
        self.tableau_table.setHorizontalHeaderLabels(["x1", "x2", "s1", "Value"])
        self.load_example_tableau()
        tableau_layout.addWidget(self.tableau_table)
        
        btn_add_row = QPushButton("+ Add Constraint")
        btn_add_row.clicked.connect(self.add_tableau_row)
        btn_add_row.setObjectName("addRowButton")
        tableau_layout.addWidget(btn_add_row)
        
        tableau_tab.setLayout(tableau_layout)
        self.tabs.addTab(tableau_tab, "Tableau Input")
        main_layout.addWidget(self.tabs)

        # Run button
        self.btn_run = QPushButton("Run Simplex Algorithm")
        self.btn_run.clicked.connect(self.run_simplex)
        self.btn_run.setObjectName("runButton")
        main_layout.addWidget(self.btn_run)

        # Results
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setPlaceholderText("Results will appear here...")
        self.result_area.setObjectName("resultArea")
        main_layout.addWidget(self.result_area)

        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            #titleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #81A1C1;
                padding: 10px;
            }
            #backButton {
                background-color: #4C566A;
                color: #D8DEE9;
                border-radius: 5px;
                padding: 5px 10px;
            }
            #backButton:hover {
                background-color: #5E81AC;
            }
            QTextEdit, QLineEdit, QTableWidget {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                font-family: monospace;
            }
            #resultArea {
                font-family: monospace;
                font-size: 14px;
            }
            QRadioButton {
                color: #D8DEE9;
                padding: 5px;
            }
            #runButton {
                background-color: #A3BE8C;
                color: #2E3440;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            #runButton:hover {
                background-color: #B5D99C;
            }
            #addRowButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    def load_example_tableau(self):
        example_data = [
            ["3", "2", "0", "0"],
            ["1", "1", "1", "4"],
            ["2", "1", "0", "5"],
            ["-1", "2", "0", "2"]
        ]
        self.tableau_table.setRowCount(len(example_data))
        for row, items in enumerate(example_data):
            for col, item in enumerate(items):
                self.tableau_table.setItem(row, col, QTableWidgetItem(item))

    def add_tableau_row(self):
        row = self.tableau_table.rowCount()
        self.tableau_table.insertRow(row)
        for col in range(self.tableau_table.columnCount()):
            self.tableau_table.setItem(row, col, QTableWidgetItem("0"))

    def parse_inputs(self):
        if self.tabs.currentIndex() == 0:  # Standard form
            try:
                c = [float(x.strip()) for x in self.entry_objective.text().split(",")]
                
                constraints = []
                for line in self.entry_constraints.toPlainText().split("\n"):
                    if not line.strip():
                        continue
                    lhs, rhs = line.split("<=")
                    constraints.append({
                        'coeffs': [float(x.strip()) for x in lhs.split(",")],
                        'rhs': float(rhs.strip())
                    })
                
                A = [con['coeffs'] for con in constraints]
                b = [con['rhs'] for con in constraints]
                
                if len(A) == 0 or len(b) == 0:
                    raise ValueError("At least one constraint required")
                if len(c) != len(A[0]):
                    raise ValueError("Objective coefficients must match constraint variables")
                
                return c, A, b, self.radio_max.isChecked()
                
            except Exception as e:
                QMessageBox.warning(self, "Input Error", f"Invalid input format: {str(e)}")
                return None
        else:  # Tableau input
            try:
                rows = self.tableau_table.rowCount()
                cols = self.tableau_table.columnCount()
                
                tableau = []
                for row in range(rows):
                    row_data = []
                    for col in range(cols):
                        item = self.tableau_table.item(row, col)
                        row_data.append(float(item.text()) if item and item.text() else 0.0)
                    tableau.append(row_data)
                
                c = tableau[0][:-1]
                A = [row[:-1] for row in tableau[1:]]
                b = [row[-1] for row in tableau[1:]]
                
                return c, A, b, True
                
            except Exception as e:
                QMessageBox.warning(self, "Input Error", f"Invalid tableau: {str(e)}")
                return None

    def run_simplex(self):
        inputs = self.parse_inputs()
        if not inputs:
            return
            
        c, A, b, maximize = inputs
        
        try:
            result = simplex(c, A, b, maximize)
            
            output = []
            output.append("=== Simplex Method Results ===")
            output.append(f"Status: {result['status'].upper()}")
            
            if result['solution'] is not None:
                output.append(f"\nOptimal Value: {result['optimal_value']:.4f}")
                output.append("\nSolution:")
                for i, x in enumerate(result['solution']):
                    output.append(f"  x{i+1} = {x:.4f}")
                
                output.append("\nBasic Variables:")
                for var in sorted(result['basis']):
                    if var < len(c):
                        output.append(f"  x{var+1}")
                    else:
                        output.append(f"  s{var-len(c)+1}")
            
            output.append(f"\nIterations: {result['iterations']}")
            self.result_area.setPlainText("\n".join(output))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run simplex: {str(e)}")

    def go_back(self):
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "LPMenu":
                self.stack.setCurrentWidget(widget)
                break