import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox,
    QSpacerItem, QSizePolicy, QRadioButton, QFileDialog
)
from PyQt6.QtCore import Qt
from algorithms.lp_algos.revised_simplex import revised_simplex

class RevisedSimplexPage(QWidget):
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
        back_layout.addWidget(self.btn_back)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Revised Simplex Method (Standard Form)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Info
        info_label = QLabel("Only supports maximization/minimization with <= constraints and b >= 0.\nIf not standard, will display an error.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(info_label)

        # File import
        file_layout = QHBoxLayout()
        self.btn_import = QPushButton("Import from Text File")
        self.btn_import.clicked.connect(self.import_from_txt)
        file_layout.addWidget(self.btn_import)
        file_layout.addWidget(QLabel("OR enter manually below:"))
        file_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(file_layout)

        # Objective function input
        main_layout.addWidget(QLabel("Objective Function (comma-separated coefficients):"))
        self.entry_objective = QLineEdit("2, 3")
        main_layout.addWidget(self.entry_objective)

        # Constraints input
        constraints_label = QLabel("Constraints (one per line, format: 'a1,a2,... <= b'):")
        main_layout.addWidget(constraints_label)
        self.entry_constraints = QTextEdit()
        self.entry_constraints.setPlainText(
            "1, 2 <= 8\n"
            "2, 1 <= 8\n"
            "1, 0 <= 3\n"
            "0, 1 <= 3"
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
        self.btn_run = QPushButton("Run Revised Simplex Algorithm")
        self.btn_run.clicked.connect(self.run_simplex)
        main_layout.addWidget(self.btn_run)

        # Results
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setPlaceholderText("Results will appear here...")
        main_layout.addWidget(self.result_area)

        self.setLayout(main_layout)

    def import_from_txt(self):
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
                    QMessageBox.warning(self, "Import Error", f"Constraint {i+1} must use '<=' operator")
                    return
                lhs, rhs = line.split("<=", 1)
                try:
                    [float(x.strip()) for x in lhs.split(",")]
                    float(rhs.strip())
                    valid_constraints.append(line)
                except ValueError:
                    QMessageBox.warning(self, "Import Error", f"Invalid numbers in constraint {i+1}")
                    return
            self.entry_objective.setText(objective)
            self.entry_constraints.setPlainText("\n".join(valid_constraints))
            QMessageBox.information(self, "Import Successful", "LP problem imported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"An unexpected error occurred:\n\n{str(e)}")

    def parse_inputs(self):
        try:
            c = [float(x.strip()) for x in self.entry_objective.text().split(",")]
            constraints = []
            for line in self.entry_constraints.toPlainText().split("\n"):
                line = line.strip()
                if not line:
                    continue
                if "<=" not in line:
                    raise ValueError(f"Constraint must use '<=' operator: {line}")
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
            for i, row in enumerate(A):
                if len(row) != len(c):
                    raise ValueError(f"Constraint {i+1} has {len(row)} coefficients but objective has {len(c)} variables")
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
            self.result_area.setPlainText("Running Revised Simplex Algorithm...\n")
            result = revised_simplex(c, A, b, maximize)
            output = []
            output.append("=== Revised Simplex Method Results ===")
            output.append(f"Status: {result['status'].upper()}")
            output.append(f"Iterations: {result['iterations']}")
            if result['status'] == 'optimal' and result['solution'] is not None:
                output.append(f"\nOptimal Value: {result['optimal_value']:.6f}")
                output.append("\nOptimal Solution:")
                for i, x in enumerate(result['solution']):
                    output.append(f"  x{i+1} = {x:.6f}")
            elif result['status'] in ['unbounded', 'infeasible']:
                output.append("\nProblem cannot be solved with the revised simplex method.")
            else:
                output.append(f"\n{result['status']}")
            self.result_area.setPlainText("\n".join(output))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run revised simplex:\n\n{str(e)}")
            self.result_area.setPlainText(f"Error: {str(e)}")

    def go_back(self):
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "LPMenu":
                self.stack.setCurrentWidget(widget)
                break