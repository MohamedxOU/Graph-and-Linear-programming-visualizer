import ast
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import a_star
from utils.graph_visualizer import afficher_graphe

class AStarPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.heuristic = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Back button
        back_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to Graph Menu")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        back_layout.addWidget(self.btn_back)
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("A* Pathfinding Algorithm")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        # Graph input tabs
        self.tabs = QTabWidget()
        
        # Graph dictionary tab
        graph_tab = QWidget()
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(QLabel("Enter graph (weighted):"))
        self.entry_graph = QTextEdit()
        self.entry_graph.setPlainText(
            "{\n"
            "    'A': {'B': 1, 'C': 3},\n"
            "    'B': {'A': 1, 'D': 5, 'E': 2},\n"
            "    'C': {'A': 3, 'F': 2},\n"
            "    'D': {'B': 5, 'H': 1},\n"
            "    'E': {'B': 2, 'H': 4},\n"
            "    'F': {'C': 2, 'G': 1},\n"
            "    'G': {'F': 1, 'H': 2},\n"
            "    'H': {'D': 1, 'E': 4, 'G': 2}\n"
            "}"
        )
        graph_layout.addWidget(self.entry_graph)
        graph_tab.setLayout(graph_layout)
        self.tabs.addTab(graph_tab, "Graph Input")

        # Heuristic input tab
        heuristic_tab = QWidget()
        heuristic_layout = QVBoxLayout()
        heuristic_layout.addWidget(QLabel("Enter heuristic values (straight-line distance to end):"))
        self.entry_heuristic = QTextEdit()
        self.entry_heuristic.setPlainText(
            "{\n"
            "    'A': 5,\n"
            "    'B': 4,\n"
            "    'C': 3,\n"
            "    'D': 2,\n"
            "    'E': 3,\n"
            "    'F': 2,\n"
            "    'G': 1,\n"
            "    'H': 0\n"
            "}"
        )
        heuristic_layout.addWidget(self.entry_heuristic)
        heuristic_tab.setLayout(heuristic_layout)
        self.tabs.addTab(heuristic_tab, "Heuristic Values")
        main_layout.addWidget(self.tabs)

        # Start and end node inputs
        node_layout = QHBoxLayout()
        node_layout.addWidget(QLabel("Start Node:"))
        self.entry_start = QLineEdit("A")
        node_layout.addWidget(self.entry_start)
        node_layout.addWidget(QLabel("End Node:"))
        self.entry_end = QLineEdit("H")
        node_layout.addWidget(self.entry_end)
        main_layout.addLayout(node_layout)

        # Run button
        self.btn_run = QPushButton("Find Path (A*)")
        self.btn_run.clicked.connect(self.run_astar)
        self.btn_run.setObjectName("runButton")
        main_layout.addWidget(self.btn_run)

        # Result display
        self.label_result = QLabel("Path will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setObjectName("resultLabel")
        main_layout.addWidget(self.label_result)

        self.setLayout(main_layout)
        
        # Apply styling
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
            #runButton {
                background-color: #D08770;
                color: #2E3440;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            #runButton:hover {
                background-color: #EBCB8B;
            }
            #resultLabel {
                font-size: 16px;
                padding: 15px;
                background-color: #3B4252;
                border-radius: 8px;
                min-height: 60px;
            }
        """)

    def run_astar(self):
        try:
            graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            heuristic = ast.literal_eval(self.entry_heuristic.toPlainText().strip())
            start = self.entry_start.text().strip()
            end = self.entry_end.text().strip()

            if not graph or not heuristic:
                QMessageBox.warning(self, "Error", "Graph and heuristic cannot be empty!")
                return
                
            if start not in graph or end not in graph:
                QMessageBox.warning(self, "Error", "Start or end node not in graph!")
                return

            path = a_star(graph, start, end, heuristic)
            
            if not path:
                self.label_result.setText(f"No path found from {start} to {end}!")
                return
                
            total_cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            result_text = f"A* Path from {start} to {end}:\n"
            result_text += " → ".join(path) + "\n"
            result_text += f"Total cost: {total_cost}"
            
            self.label_result.setText(result_text)
            afficher_graphe(
                graph,
                parcours=path,
                titre=f"A*: {start} to {end} (Cost: {total_cost})",
                weighted=True
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def go_back(self):
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break