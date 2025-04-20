import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox,
    QSpacerItem, QSizePolicy, QRadioButton, QFileDialog
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

        # File import section
        file_layout = QHBoxLayout()
        self.btn_import = QPushButton("Import from Text File")
        self.btn_import.clicked.connect(self.import_from_txt)
        self.btn_import.setObjectName("importButton")
        file_layout.addWidget(self.btn_import)
        file_layout.addWidget(QLabel("OR enter manually below:"))
        file_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(file_layout)
        
        # Objective function input
        main_layout.addWidget(QLabel("Objective Function (comma-separated coefficients):"))
        self.entry_objective = QLineEdit("3, 2")
        main_layout.addWidget(self.entry_objective)
        
        # Constraints input
        main_layout.addWidget(QLabel("Constraints (one per line, format: 'a1,a2,... <= b'):"))
        self.entry_constraints = QTextEdit()
        self.entry_constraints.setPlainText(
            "1, 1 <= 4\n"
            "2, 1 <= 5\n"
            "-1, 2 <= 2"
        )
        main_layout.addWidget(self.entry_constraints)
        
        # Optimization type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Optimization:"))
        self.radio_max = QRadioButton("Maximize")
        self.radio_max.setChecked(True)
        self.radio_min = QRadioButton("Minimize")
        type_layout.addWidget(self.radio_max)
        type_layout.addWidget(self.radio_min)
        type_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(type_layout)

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
            QTextEdit, QLineEdit {
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
            #importButton {
                background-color: #D08770;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            #importButton:hover {
                background-color: #EBCB8B;
            }
        """)

    def import_from_txt(self):
        """Import LP problem from text file in standard form"""
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, 
                "Import LP Problem", 
                "", 
                "Text Files (*.txt);;All Files (*)"
            )
            
            if not file_name:
                return
                
            with open(file_name, 'r') as file:
                content = file.read()
                
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            if len(lines) < 2:
                QMessageBox.warning(self, "Import Error", "File must contain at least 2 lines (objective and constraints)")
                return
                
            # Validate objective function
            try:
                objective = lines[0]
                [float(x.strip()) for x in objective.split(",")]
            except ValueError:
                QMessageBox.warning(self, "Import Error", "First line must contain comma-separated numbers for objective function")
                return
                
            # Validate constraints
            valid_constraints = []
            for i, line in enumerate(lines[1:]):
                if "<=" not in line:
                    QMessageBox.warning(self, "Import Error", f"Constraint {i+1} missing '<=' symbol")
                    return
                    
                lhs, rhs = line.split("<=", 1)
                try:
                    coeffs = [float(x.strip()) for x in lhs.split(",")]
                    float(rhs.strip())
                    valid_constraints.append(line)
                except ValueError:
                    QMessageBox.warning(self, "Import Error", f"Invalid numbers in constraint {i+1}")
                    return
            
            # Update UI if validation passed
            self.entry_objective.setText(objective)
            self.entry_constraints.setPlainText("\n".join(valid_constraints))
            
            QMessageBox.information(
                self, 
                "Import Successful", 
                "LP problem imported successfully!\n\n"
                f"Objective: {objective}\n"
                f"Constraints: {len(valid_constraints)} loaded"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Import Error", 
                f"An unexpected error occurred:\n\n{str(e)}"
            )

    def parse_inputs(self):
        try:
            c = [float(x.strip()) for x in self.entry_objective.text().split(",")]
            
            constraints = []
            for line in self.entry_constraints.toPlainText().split("\n"):
                line = line.strip()
                if not line:
                    continue
                    
                if "<=" not in line:
                    raise ValueError(f"Constraint missing '<=' symbol: {line}")
                    
                lhs, rhs = line.split("<=", 1)
                constraints.append({
                    'coeffs': [float(x.strip()) for x in lhs.split(",")],
                    'rhs': float(rhs.strip())
                })
            
            A = [con['coeffs'] for con in constraints]
            b = [con['rhs'] for con in constraints]
            
            if len(A) == 0 or len(b) == 0:
                raise ValueError("At least one constraint required")
            if len(c) != len(A[0]):
                raise ValueError(f"Objective has {len(c)} coefficients but constraints have {len(A[0])} variables")
            
            return c, A, b, self.radio_max.isChecked()
            
        except Exception as e:
            QMessageBox.warning(self, "Input Error", f"Invalid input format:\n\n{str(e)}")
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
            QMessageBox.critical(self, "Error", f"Failed to run simplex:\n\n{str(e)}")

    def go_back(self):
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "LPMenu":
                self.stack.setCurrentWidget(widget)
                break