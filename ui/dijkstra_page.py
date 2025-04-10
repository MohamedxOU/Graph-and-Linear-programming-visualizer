import ast
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import dijkstra, reconstruct_path_dk
import heapq

class DijkstraPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.current_figure = None
        self.animation = None
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
            
            QTextEdit, QTableWidget {
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

            # Close previous visualization if exists
            if self.current_figure:
                plt.close(self.current_figure)
            if self.animation and self.animation.event_source:
                self.animation.event_source.stop()

            # Run Dijkstra's algorithm
            distances, previous_nodes = dijkstra(graph, start)
            
            if distances[end] == float('inf'):
                self.label_result.setText(f"No path exists from {start} to {end}!")
                return
                
            path = reconstruct_path_dk(previous_nodes, start, end)
            total_distance = distances[end]
            
            result_text = f"Shortest path from {start} to {end}:\n"
            result_text += " → ".join(path) + "\n"
            result_text += f"Total distance: {total_distance}"
            
            self.label_result.setText(result_text)
            
            # Create visualization
            self.current_figure, self.animation = self.dijkstra_visualizer(graph, start, end, distances, previous_nodes)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def dijkstra_visualizer(self, graph, start, end, distances, previous_nodes):
        """Visualize Dijkstra's algorithm with step-by-step animation"""
        # Create the graph structure
        G = nx.DiGraph() if nx.is_directed(nx.DiGraph(graph)) else nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Reconstruct the exploration order
        path = reconstruct_path_dk(previous_nodes, start, end)
        visited_order = []
        priority_queue = [(0, start)]
        visited = set()
        
        # This will store the state at each step
        steps = []
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_node in visited:
                continue
                
            visited.add(current_node)
            visited_order.append(current_node)
            steps.append((current_node, distances.copy(), previous_nodes.copy()))
            
            for neighbor, weight in graph.get(current_node, {}).items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # Animation update function
        def update(frame):
            ax.clear()
            
            if frame < len(steps):
                current_node, current_distances, current_previous = steps[frame]
                
                # Prepare node colors and labels
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node == current_node:
                        node_colors.append('red')  # Current node
                    elif node in visited_order[:frame]:
                        node_colors.append('lightgreen')  # Visited nodes
                    else:
                        node_colors.append('lightgray')  # Unvisited nodes
                    
                    # Show distance on each node
                    dist = current_distances.get(node, float('inf'))
                    node_labels[node] = f"{node}\n({dist if dist != float('inf') else '∞'})"
                
                # Prepare edge colors
                edge_colors = []
                edge_labels = {}
                for u, v, data in G.edges(data=True):
                    if u == current_node and v in graph[current_node]:
                        edge_colors.append('red')
                    else:
                        edge_colors.append('gray')
                    edge_labels[(u, v)] = str(data['weight'])
                
                # Highlight the current best path
                path_edges = []
                for node in visited_order[:frame+1]:
                    if current_previous[node] is not None:
                        path_edges.append((current_previous[node], node))
                
                # Draw the graph
                nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=10)
                
                # Draw all edges
                nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2)
                
                # Highlight path edges
                nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, 
                                     edge_color='blue', width=3)
                
                # Draw edge labels
                nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)
                
                ax.set_title(f"Step {frame+1}/{len(steps)}: Visiting {current_node}\n"
                           f"Current distance to {end}: {current_distances.get(end, float('inf'))}")
            else:
                # Final state - show complete path
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node in path:
                        node_colors.append('lightblue')
                    elif node in visited_order:
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')
                    
                    dist = distances.get(node, float('inf'))
                    node_labels[node] = f"{node}\n({dist if dist != float('inf') else '∞'})"
                
                # Draw the graph
                nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=10)
                
                # Draw all edges
                nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=1)
                
                # Highlight path edges
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, 
                                     edge_color='blue', width=3)
                
                # Draw edge labels
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)
                
                ax.set_title(f"Shortest path found!\n{start} to {end}: {distances[end]}")
            
            ax.axis('off')
        
        # Create animation
        ani = FuncAnimation(fig, update, frames=len(steps)+1,
                          interval=1500, repeat=False)  # 1.5 seconds per step
        
        plt.show(block=False)
        return fig, ani
            
    def go_back(self):
        """Return to the graph menu"""
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break