import ast
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import dijkstra, reconstruct_path
from utils.graph_visualizer import afficher_graphe

class DijkstraPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Back button
        back_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to Graph Menu")
        self.btn_back.clicked.connect(self.go_back)
        back_layout.addWidget(self.btn_back)
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Dijkstra's Shortest Path Algorithm")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # Graph input tabs
        self.tabs = QTabWidget()
        
        # Dictionary input tab
        dict_tab = QWidget()
        dict_layout = QVBoxLayout()
        dict_layout.addWidget(QLabel("Enter weighted graph as dictionary:"))
        self.entry_graph = QTextEdit()
        self.entry_graph.setPlainText(
            "{\n"
            "    'A': {'B': 1, 'C': 4},\n"
            "    'B': {'A': 1, 'D': 2, 'E': 5},\n"
            "    'C': {'A': 4, 'F': 3},\n"
            "    'D': {'B': 2},\n"
            "    'E': {'B': 5, 'H': 2},\n"
            "    'F': {'C': 3, 'G': 1},\n"
            "    'G': {'F': 1, 'H': 3},\n"
            "    'H': {'E': 2, 'G': 3}\n"
            "}"
        )
        dict_layout.addWidget(self.entry_graph)
        dict_tab.setLayout(dict_layout)
        self.tabs.addTab(dict_tab, "Dictionary Input")

        # Table input tab
        table_tab = QWidget()
        table_layout = QVBoxLayout()
        table_layout.addWidget(QLabel("Enter weighted graph as adjacency list:"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Node", "Neighbor", "Weight"])
        self.load_example_data()
        table_layout.addWidget(self.table)
        
        btn_add_row = QPushButton("+ Add Row")
        btn_add_row.clicked.connect(self.add_table_row)
        table_layout.addWidget(btn_add_row)
        
        table_tab.setLayout(table_layout)
        self.tabs.addTab(table_tab, "Table Input")
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
        self.btn_run = QPushButton("Find Shortest Path")
        self.btn_run.clicked.connect(self.run_dijkstra)
        self.btn_run.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;"
        )
        main_layout.addWidget(self.btn_run)

        # Result display
        self.label_result = QLabel("Shortest path will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setStyleSheet(
            "background-color: #f0f0f0; padding: 15px; border-radius: 5px;"
        )
        main_layout.addWidget(self.label_result)

        self.setLayout(main_layout)

    def load_example_data(self):
        example_data = [
            ("A", "B", 1),
            ("A", "C", 4),
            ("B", "D", 2),
            ("B", "E", 5),
            ("C", "F", 3),
            ("E", "H", 2),
            ("F", "G", 1),
            ("G", "H", 3)
        ]
        
        self.table.setRowCount(len(example_data))
        for row, (node, neighbor, weight) in enumerate(example_data):
            self.table.setItem(row, 0, QTableWidgetItem(node))
            self.table.setItem(row, 1, QTableWidgetItem(neighbor))
            self.table.setItem(row, 2, QTableWidgetItem(str(weight)))

    def add_table_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem("1"))  # Default weight

    def get_graph_from_table(self):
        graph = {}
        for row in range(self.table.rowCount()):
            node_item = self.table.item(row, 0)
            neighbor_item = self.table.item(row, 1)
            weight_item = self.table.item(row, 2)
            
            if node_item and neighbor_item:
                node = node_item.text().strip()
                neighbor = neighbor_item.text().strip()
                try:
                    weight = float(weight_item.text()) if weight_item else 1
                except ValueError:
                    weight = 1
                
                if node and neighbor:
                    if node not in graph:
                        graph[node] = {}
                    graph[node][neighbor] = weight
        return graph

    def run_dijkstra(self):
        try:
            # Get graph from current tab
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            else:  # Table tab
                graph = self.get_graph_from_table()
            
            start = self.entry_start.text().strip()
            end = self.entry_end.text().strip()

            if not graph:
                QMessageBox.warning(self, "Error", "Graph cannot be empty!")
                return
                
            if not start or not end:
                QMessageBox.warning(self, "Error", "Please enter both start and end nodes!")
                return
                
            if start not in graph or end not in graph:
                QMessageBox.warning(self, "Error", "Start or end node not in graph!")
                return

            distances, previous_nodes = dijkstra(graph, start)
            
            if distances[end] == float('inf'):
                self.label_result.setText(f"No path exists from {start} to {end}!")
                return
                
            path = reconstruct_path(previous_nodes, start, end)
            total_distance = distances[end]
            
            result_text = f"Shortest path from {start} to {end}:\n"
            result_text += " → ".join(path) + "\n"
            result_text += f"Total distance: {total_distance}"
            
            self.label_result.setText(result_text)
            
            # Visualize with highlighted path
            afficher_graphe(
                graph,
                parcours=path,
                titre=f"Dijkstra: {start} to {end} (Distance: {total_distance})",
                weighted=True
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def go_back(self):
        """Return to the graph menu"""
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break