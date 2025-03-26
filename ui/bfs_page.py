import ast
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
                            QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import bfs
from utils.graph_visualizer import afficher_graphe

class BFSPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}  # Store the current graph
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Back button row
        back_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to Graph Menu")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        back_layout.addWidget(self.btn_back)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Breadth-First Search (BFS) Algorithm")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        # Graph input tabs
        self.tabs = QTabWidget()
        
        # Dictionary input tab
        dict_tab = QWidget()
        dict_layout = QVBoxLayout()
        dict_layout.addWidget(QLabel("Enter graph as dictionary:"))
        self.entry_graphe = QTextEdit()
        self.entry_graphe.setPlainText(
            "{\n"
            "    'A': ['B', 'C'],\n"
            "    'B': ['A', 'D', 'E'],\n"
            "    'C': ['A', 'F', 'G'],\n"
            "    'D': ['B'],\n"
            "    'E': ['B', 'H'],\n"
            "    'F': ['C'],\n"
            "    'G': ['C'],\n"
            "    'H': ['E']\n"
            "}"
        )
        dict_layout.addWidget(self.entry_graphe)
        dict_tab.setLayout(dict_layout)
        self.tabs.addTab(dict_tab, "Dictionary Input")

        # Table input tab
        table_tab = QWidget()
        table_layout = QVBoxLayout()
        table_layout.addWidget(QLabel("Enter graph as adjacency list:"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Node", "Connected Nodes (comma separated)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.load_example_data()
        table_layout.addWidget(self.table)
        
        btn_add_row = QPushButton("+ Add Row")
        btn_add_row.clicked.connect(self.add_table_row)
        btn_add_row.setObjectName("addRowButton")
        table_layout.addWidget(btn_add_row)
        
        table_tab.setLayout(table_layout)
        self.tabs.addTab(table_tab, "Table Input")
        main_layout.addWidget(self.tabs)

        # Starting node input
        node_layout = QHBoxLayout()
        node_layout.addWidget(QLabel("Starting Node:"))
        self.entry_noeud = QLineEdit("A")
        self.entry_noeud.setMaximumWidth(100)
        node_layout.addWidget(self.entry_noeud)
        node_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(node_layout)

        # Run button
        self.button_run_bfs = QPushButton("Run BFS Algorithm")
        self.button_run_bfs.clicked.connect(self.run_bfs)
        self.button_run_bfs.setObjectName("runButton")
        main_layout.addWidget(self.button_run_bfs)

        # Result display
        self.label_result = QLabel("BFS traversal will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
            
            QTextEdit, QLineEdit, QTableWidget {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                font-family: monospace;
            }
            
            QTabWidget::pane {
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            
            QTabBar::tab {
                background-color: #3B4252;
                color: #D8DEE9;
                padding: 8px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background-color: #434C5E;
                border-bottom: 2px solid #81A1C1;
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
            
            #resultLabel {
                font-size: 16px;
                padding: 15px;
                background-color: #3B4252;
                border-radius: 8px;
                min-height: 60px;
            }
        """)

    def load_example_data(self):
        """Load example data into the table"""
        example_data = [
            ("A", "B, C"),
            ("B", "A, D, E"),
            ("C", "A, F, G"),
            ("D", "B"),
            ("E", "B, H"),
            ("F", "C"),
            ("G", "C"),
            ("H", "E")
        ]
        
        self.table.setRowCount(len(example_data))
        for row, (node, connections) in enumerate(example_data):
            self.table.setItem(row, 0, QTableWidgetItem(node))
            self.table.setItem(row, 1, QTableWidgetItem(connections))

    def add_table_row(self):
        """Add a new empty row to the table"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))

    def get_graph_from_table(self):
        """Convert table data to graph dictionary"""
        graph = {}
        for row in range(self.table.rowCount()):
            node_item = self.table.item(row, 0)
            connections_item = self.table.item(row, 1)
            
            if node_item and (node := node_item.text().strip()):
                connections = []
                if connections_item:
                    connections = [c.strip() for c in connections_item.text().split(",") if c.strip()]
                graph[node] = connections
        return graph

    def run_bfs(self):
        try:
            # Get graph from current tab
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graphe = ast.literal_eval(self.entry_graphe.toPlainText().strip())
            else:  # Table tab
                graphe = self.get_graph_from_table()
            
            noeud_depart = self.entry_noeud.text().strip()

            if not graphe:
                QMessageBox.warning(self, "Error", "Graph cannot be empty!")
                return
                
            if not noeud_depart:
                QMessageBox.warning(self, "Error", "Please enter a starting node!")
                return
                
            if noeud_depart not in graphe:
                QMessageBox.warning(self, "Error", f"Starting node '{noeud_depart}' not in graph!")
                return
            
            resultat = bfs(graphe, noeud_depart)
            self.label_result.setText(f"BFS Traversal:\n{' → '.join(resultat)}")
            afficher_graphe(graphe, parcours=resultat, titre="BFS")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def go_back(self):
        """Return to the graph menu"""
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break