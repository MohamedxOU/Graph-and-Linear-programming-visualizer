import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox,
    QSpacerItem, QSizePolicy, QRadioButton, QFileDialog
)
from PyQt6.QtCore import Qt
from algorithms.lp_algos.simplex import two_phase_simplex

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
        title = QLabel("Two-Phase Simplex Method for Linear Programming")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        # Information label
        info_label = QLabel("Supports mixed constraints: <=, =, >= (artificial variables handled automatically)")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setObjectName("infoLabel")
        main_layout.addWidget(info_label)

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
        self.entry_objective = QLineEdit("3, 2, 1")
        main_layout.addWidget(self.entry_objective)
        
        # Constraints input with examples
        constraints_label = QLabel("Constraints (one per line, format: 'a1,a2,... OP b' where OP is <=, =, or >=):")
        main_layout.addWidget(constraints_label)
        
        self.entry_constraints = QTextEdit()
        self.entry_constraints.setPlainText(
            "1, 1, 1 = 6\n"
            "2, 1, 0 >= 4\n"
            "1, 0, 1 <= 5"
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
        self.btn_run = QPushButton("Run Two-Phase Simplex Algorithm")
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
            #infoLabel {
                font-size: 12px;
                color: #88C0D0;
                font-style: italic;
                padding: 5px;
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
        """Import LP problem from text file supporting mixed constraint types"""
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
                
            # Validate constraints with mixed operators
            valid_constraints = []
            constraint_operators = ['<=', '>=', '=']
            
            for i, line in enumerate(lines[1:]):
                found_operator = False
                for op in constraint_operators:
                    if op in line:
                        lhs, rhs = line.split(op, 1)
                        try:
                            coeffs = [float(x.strip()) for x in lhs.split(",")]
                            float(rhs.strip())
                            valid_constraints.append(line)
                            found_operator = True
                            break
                        except ValueError:
                            QMessageBox.warning(self, "Import Error", f"Invalid numbers in constraint {i+1}")
                            return
                
                if not found_operator:
                    QMessageBox.warning(self, "Import Error", f"Constraint {i+1} missing valid operator (<=, =, >=)")
                    return
            
            # Update UI if validation passed
            self.entry_objective.setText(objective)
            self.entry_constraints.setPlainText("\n".join(valid_constraints))
            
            # Count constraint types for user info
            constraint_counts = {'<=': 0, '=': 0, '>=': 0}
            for constraint in valid_constraints:
                for op in constraint_operators:
                    if op in constraint:
                        constraint_counts[op] += 1
                        break
            
            info_text = f"LP problem imported successfully!\n\n"
            info_text += f"Objective: {objective}\n"
            info_text += f"Total constraints: {len(valid_constraints)}\n"
            info_text += f"  <= constraints: {constraint_counts['<=']}\n"
            info_text += f"  =  constraints: {constraint_counts['=']}\n"
            info_text += f"  >= constraints: {constraint_counts['>=']}"
            
            if constraint_counts['='] > 0 or constraint_counts['>='] > 0:
                info_text += "\n\nNote: Artificial variables will be used for = and >= constraints."
            
            QMessageBox.information(self, "Import Successful", info_text)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Import Error", 
                f"An unexpected error occurred:\n\n{str(e)}"
            )

    def parse_inputs(self):
        """Parse inputs and extract constraint types"""
        try:
            c = [float(x.strip()) for x in self.entry_objective.text().split(",")]
            
            constraints = []
            constraint_types = []
            constraint_operators = ['<=', '>=', '=']  # Order matters for parsing
            
            for line in self.entry_constraints.toPlainText().split("\n"):
                line = line.strip()
                if not line:
                    continue
                
                found_operator = False
                for op in constraint_operators:
                    if op in line:
                        lhs, rhs = line.split(op, 1)
                        constraints.append({
                            'coeffs': [float(x.strip()) for x in lhs.split(",")],
                            'rhs': float(rhs.strip())
                        })
                        constraint_types.append(op)
                        found_operator = True
                        break
                
                if not found_operator:
                    raise ValueError(f"Constraint missing valid operator (<=, =, >=): {line}")
            
            A = [con['coeffs'] for con in constraints]
            b = [con['rhs'] for con in constraints]
            
            if len(A) == 0 or len(b) == 0:
                raise ValueError("At least one constraint required")
            if len(c) != len(A[0]):
                raise ValueError(f"Objective has {len(c)} coefficients but constraints have {len(A[0])} variables")
            
            # Check for consistency in number of variables
            for i, row in enumerate(A):
                if len(row) != len(c):
                    raise ValueError(f"Constraint {i+1} has {len(row)} coefficients but objective has {len(c)} variables")
            
            return c, A, b, constraint_types, self.radio_max.isChecked()
            
        except Exception as e:
            QMessageBox.warning(self, "Input Error", f"Invalid input format:\n\n{str(e)}")
            return None

    def run_simplex(self):
        """Run the two-phase simplex algorithm"""
        inputs = self.parse_inputs()
        if not inputs:
            return
            
        c, A, b, constraint_types, maximize = inputs
        
        try:
            self.result_area.setPlainText("Running Two-Phase Simplex Algorithm...\n")
            
            result = two_phase_simplex(c, A, b, constraint_types, maximize)
            
            output = []
            output.append("=== Two-Phase Simplex Method Results ===")
            output.append(f"Status: {result['status'].upper()}")
            
            # Show phase information
            output.append(f"\nPhase I Iterations: {result['phase1_iterations']}")
            output.append(f"Phase II Iterations: {result['phase2_iterations']}")
            output.append(f"Total Iterations: {result['iterations']}")
            
            # Show constraint analysis
            constraint_counts = {'<=': 0, '=': 0, '>=': 0}
            for ct in constraint_types:
                constraint_counts[ct] += 1
            
            output.append(f"\nConstraint Analysis:")
            output.append(f"  <= constraints: {constraint_counts['<=']}")
            output.append(f"  =  constraints: {constraint_counts['=']}")
            output.append(f"  >= constraints: {constraint_counts['>=']}")
            
            if constraint_counts['='] > 0 or constraint_counts['>='] > 0:
                artificial_count = constraint_counts['='] + constraint_counts['>=']
                output.append(f"  Artificial variables used: {artificial_count}")
            
            if result['solution'] is not None:
                output.append(f"\nOptimal Value: {result['optimal_value']:.6f}")
                output.append("\nOptimal Solution:")
                for i, x in enumerate(result['solution']):
                    output.append(f"  x{i+1} = {x:.6f}")
                
                # Show which constraints are binding (if solution exists)
                if result['status'] == 'optimal':
                    output.append("\nConstraint Analysis:")
                    for i, (constraint_type, rhs) in enumerate(zip(constraint_types, b)):
                        lhs_value = sum(A[i][j] * result['solution'][j] for j in range(len(result['solution'])))
                        slack = abs(rhs - lhs_value)
                        if slack < 1e-6:
                            status = "BINDING"
                        else:
                            status = f"Slack: {slack:.6f}"
                        output.append(f"  Constraint {i+1} ({constraint_type}): {status}")
            
            elif result['status'] == 'infeasible':
                output.append("\nThe problem is INFEASIBLE.")
                output.append("No solution exists that satisfies all constraints.")
                if result['phase1_iterations'] > 0:
                    output.append("Phase I could not eliminate all artificial variables.")
            
            elif result['status'] == 'unbounded':
                output.append("\nThe problem is UNBOUNDED.")
                output.append("The objective function can be improved indefinitely.")
            
            self.result_area.setPlainText("\n".join(output))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run two-phase simplex:\n\n{str(e)}")
            self.result_area.setPlainText(f"Error: {str(e)}")

    def go_back(self):
        """Navigate back to LP Menu"""
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "LPMenu":
                self.stack.setCurrentWidget(widget)
                break