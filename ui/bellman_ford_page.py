import ast
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import bellman_ford, reconstruct_path_bf

class BellmanFordPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.current_figure = None
        self.animation = None
        self.paused = False
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
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Bellman-Ford Shortest Path Algorithm")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        # File import button
        import_layout = QHBoxLayout()
        self.btn_import = QPushButton("Import Graph from File")
        self.btn_import.clicked.connect(self.import_from_file)
        self.btn_import.setObjectName("importButton")
        import_layout.addWidget(self.btn_import)
        import_layout.addWidget(QLabel("OR enter manually below:"))
        import_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(import_layout)

        # Graph input tabs
        self.tabs = QTabWidget()
        
        # Dictionary input tab
        dict_tab = QWidget()
        dict_layout = QVBoxLayout()
        dict_layout.addWidget(QLabel("Enter weighted graph as dictionary:"))
        self.entry_graph = QTextEdit()
        self.entry_graph.setPlainText(
            "{\n"
            "    'A': {'B': -1, 'C': 4},\n"
            "    'B': {'C': 3, 'D': 2, 'E': 2},\n"
            "    'C': {},\n"
            "    'D': {'B': 1, 'C': 5},\n"
            "    'E': {'D': -3}\n"
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

        # Start and end node inputs
        node_layout = QHBoxLayout()
        node_layout.addWidget(QLabel("Start Node:"))
        self.entry_start = QLineEdit("A")
        self.entry_start.setMaximumWidth(100)
        node_layout.addWidget(self.entry_start)
        
        node_layout.addWidget(QLabel("End Node:"))
        self.entry_end = QLineEdit("E")
        self.entry_end.setMaximumWidth(100)
        node_layout.addWidget(self.entry_end)
        
        node_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(node_layout)

        # Control buttons
        control_layout = QHBoxLayout()
        self.btn_run = QPushButton("Find Shortest Path")
        self.btn_run.clicked.connect(self.run_bellman_ford)
        self.btn_run.setObjectName("runButton")
        control_layout.addWidget(self.btn_run)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_pause.setObjectName("controlButton")
        self.btn_pause.setEnabled(False)
        control_layout.addWidget(self.btn_pause)

        self.btn_reset = QPushButton("Reset Layout")
        self.btn_reset.clicked.connect(self.reset_layout)
        self.btn_reset.setObjectName("controlButton")
        self.btn_reset.setEnabled(False)
        control_layout.addWidget(self.btn_reset)
        main_layout.addLayout(control_layout)

        # Scrollable result display
        self.result_display = QTextEdit()
        self.result_display.setObjectName("resultDisplay")
        self.result_display.setReadOnly(True)
        self.result_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.result_display.setPlaceholderText("Shortest path will appear here...")
        main_layout.addWidget(self.result_display, stretch=1)

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
            #importButton {
                background-color: #D08770;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            #importButton:hover {
                background-color: #EBCB8B;
            }
            #controlButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            #controlButton:hover {
                background-color: #81A1C1;
            }
            #resultDisplay {
                font-family: monospace;
                font-size: 14px;
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 8px;
                min-height: 100px;
            }
        """)

    def load_example_data(self):
        example_data = [
            ("A", "B", -1),
            ("A", "C", 4),
            ("B", "C", 3),
            ("B", "D", 2),
            ("B", "E", 2),
            ("D", "B", 1),
            ("D", "C", 5),
            ("E", "D", -3)
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

    def import_from_file(self):
        """Import graph from a text file in dictionary format"""
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Import Graph Dictionary",
                "",
                "Text Files (*.txt);;All Files (*)"
            )
            
            if not file_name:
                return
                
            with open(file_name, 'r') as file:
                content = file.read()
                
            # Validate the content is a proper dictionary
            try:
                graph_dict = ast.literal_eval(content)
                if not isinstance(graph_dict, dict):
                    raise ValueError("File content must be a dictionary")
                    
                # Update the dictionary input tab
                self.entry_graph.setPlainText(content)
                self.tabs.setCurrentIndex(0)  # Switch to dictionary tab
                
                QMessageBox.information(
                    self,
                    "Import Successful",
                    "Graph dictionary imported successfully!"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Import Error",
                    f"Invalid graph dictionary format:\n\n{str(e)}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Failed to import file:\n\n{str(e)}"
            )

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

    def run_bellman_ford(self):
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

            # Reset pause state
            self.paused = False
            self.btn_pause.setText("Pause")
            self.btn_pause.setEnabled(True)
            self.btn_reset.setEnabled(True)

            # Run Bellman-Ford algorithm
            distances, predecessors = bellman_ford(graph, start)
            
            if distances is None:
                self.result_display.setPlainText("Negative weight cycle detected! No shortest path exists.")
                return
                
            path = reconstruct_path_bf(predecessors, start, end)
            
            if not path:
                result_text = f"No path exists from {start} to {end}"
            else:
                result_text = f"Shortest path from {start} to {end}:\n"
                result_text += " → ".join(path) + "\n\n"
                result_text += f"Total distance: {distances[end]}\n\n"
                result_text += "All distances:\n"
                for node in sorted(distances.keys()):
                    dist = distances[node]
                    result_text += f"{node}: {dist if dist != float('inf') else '∞'}\n"
            
            # Display in scrollable area
            self.result_display.setPlainText(result_text)
            self.result_display.ensureCursorVisible()  # Auto-scroll to bottom
            
            # Create visualization
            self.current_figure, self.animation = self.bellman_ford_visualizer(graph, start, end, distances, predecessors)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")
            self.result_display.setPlainText(f"Error: {str(e)}")

    def toggle_pause(self):
        """Toggle animation pause state"""
        if self.animation:
            self.paused = not self.paused
            if self.paused:
                self.animation.event_source.stop()
                self.btn_pause.setText("Resume")
            else:
                self.animation.event_source.start()
                self.btn_pause.setText("Pause")

    def reset_layout(self):
        """Reset graph layout to default spring layout"""
        if hasattr(self, 'pos') and self.current_figure:
            # Recalculate positions using spring layout
            G = nx.DiGraph() if nx.is_directed(nx.DiGraph(self.graph)) else nx.Graph()
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            else:  # Table tab
                graph = self.get_graph_from_table()
            
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)
            
            self.pos = nx.spring_layout(G)
            
            # Redraw with new positions
            if hasattr(self, 'update'):
                self.update(self.current_frame)
                self.current_figure.canvas.draw_idle()

    def bellman_ford_visualizer(self, graph, start, end, distances, predecessors):
        """Visualize Bellman-Ford algorithm with step-by-step animation"""
        G = nx.DiGraph() if nx.is_directed(nx.DiGraph(graph)) else nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        
        # Store positions as instance variables for access in callbacks
        self.pos = nx.spring_layout(G)
        self.G = G
        self.current_frame = 0
        
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig
        
        # Reconstruct the steps of Bellman-Ford
        steps = []
        current_distances = {node: float('inf') for node in graph}
        current_distances[start] = 0
        current_predecessors = {node: None for node in graph}
        
        # For visualization, we'll track each relaxation
        for i in range(len(graph) - 1):
            updated = False
            for u in graph:
                for v, weight in graph[u].items():
                    if current_distances[u] + weight < current_distances[v]:
                        old_dist = current_distances[v]
                        current_distances[v] = current_distances[u] + weight
                        current_predecessors[v] = u
                        steps.append((i+1, u, v, weight, current_distances.copy(), current_predecessors.copy(), old_dist))
                        updated = True
            
            if not updated:
                break
        
        # Check for negative cycles (visualization step)
        has_negative_cycle = False
        for u in graph:
            for v, weight in graph[u].items():
                if current_distances[u] + weight < current_distances[v]:
                    steps.append((-1, u, v, weight, None, None, None))  # Special frame for cycle detection
                    has_negative_cycle = True
                    break
            if has_negative_cycle:
                break
        
        # Animation update function
        def update(frame):
            self.current_frame = frame
            ax.clear()
            
            if frame < len(steps):
                iteration, u, v, weight, current_dists, current_preds, old_dist = steps[frame]
                
                if iteration == -1:  # Negative cycle frame
                    # Draw the graph with cycle highlighted
                    node_colors = ['lightgray' for _ in G.nodes()]
                    edge_colors = ['gray' for _ in G.edges()]
                    
                    # Highlight the problematic edge
                    for i, edge in enumerate(G.edges()):
                        if edge == (u, v):
                            edge_colors[i] = 'red'
                    
                    nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                    nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                    nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=2)
                    
                    # Draw edge labels
                    edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                    nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                    
                    ax.set_title("Negative cycle detected!\n"
                               f"Edge {u}→{v} (weight: {weight}) creates negative cycle")
                else:
                    # Prepare node colors
                    node_colors = []
                    for node in G.nodes():
                        if node == u or node == v:
                            node_colors.append('red')  # Current nodes being processed
                        elif current_dists[node] != float('inf'):
                            node_colors.append('lightgreen')  # Nodes with known distances
                        else:
                            node_colors.append('lightgray')  # Unprocessed nodes
                    
                    # Prepare edge colors and widths
                    edge_colors = []
                    edge_widths = []
                    for edge in G.edges():
                        if edge == (u, v):
                            edge_colors.append('red')
                            edge_widths.append(3)
                        else:
                            edge_colors.append('gray')
                            edge_widths.append(1)
                    
                    # Draw the graph
                    nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                    nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                    nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
                    
                    # Draw edge labels
                    edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                    nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                    
                    # Display distance updates
                    dist_text = f"Updated {v}'s distance:\n"
                    dist_text += f"Old: {old_dist if old_dist != float('inf') else '∞'}\n"
                    dist_text += f"New: {current_dists[v]}\n"
                    dist_text += f"Via: {u} (distance {current_dists[u]})"
                    
                    ax.set_title(f"Iteration {iteration}: Relaxing edge {u}→{v} (weight: {weight})\n{dist_text}")
            else:
                # Final state - show complete results
                if has_negative_cycle:
                    node_colors = ['lightgray' for _ in G.nodes()]
                    edge_colors = ['gray' for _ in G.edges()]
                    
                    nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                    nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                    nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=2)
                    
                    # Draw edge labels
                    edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                    nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                    
                    ax.set_title("Negative weight cycle detected!\nNo shortest paths exist")
                else:
                    # Highlight the shortest path
                    path = reconstruct_path_bf(predecessors, start, end)
                    path_edges = list(zip(path[:-1], path[1:]))
                    
                    # Prepare node colors
                    node_colors = []
                    for node in G.nodes():
                        if node == start:
                            node_colors.append('green')  # Start node
                        elif node == end:
                            node_colors.append('red')  # End node
                        elif node in path:
                            node_colors.append('lightblue')  # Path nodes
                        else:
                            node_colors.append('lightgray')  # Other nodes
                    
                    # Prepare edge colors and widths
                    edge_colors = []
                    edge_widths = []
                    for edge in G.edges():
                        if edge in path_edges:
                            edge_colors.append('blue')
                            edge_widths.append(3)
                        else:
                            edge_colors.append('gray')
                            edge_widths.append(1)
                    
                    # Draw the graph
                    nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                    nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                    nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
                    
                    # Draw edge labels
                    edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                    nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                    
                    # Display distances
                    dist_text = f"Shortest path from {start} to {end}: {distances[end]}\n"
                    dist_text += f"Path: {' → '.join(path)}"
                    
                    ax.set_title(f"Bellman-Ford Complete!\n{dist_text}")
            
            ax.axis('off')
        
        # Store update function for reset
        self.update = update
        
        # Mouse event handlers for dragging nodes
        def on_press(event):
            if event.inaxes != ax or not self.paused:
                return
            
            # Find if a node was clicked
            for node in G.nodes():
                x, y = self.pos[node]
                if (x - event.xdata)**2 + (y - event.ydata)**2 < 0.01:  # Click radius
                    self.selected_node = node
                    self.offset = (x - event.xdata, y - event.ydata)
                    break
    
        def on_motion(event):
            if not hasattr(self, 'selected_node') or self.selected_node is None or event.inaxes != ax:
                return
            
            # Update node position
            self.pos[self.selected_node] = (event.xdata + self.offset[0], event.ydata + self.offset[1])
            
            # Redraw the current frame
            update(self.current_frame)
            fig.canvas.draw_idle()
    
        def on_release(event):
            if hasattr(self, 'selected_node'):
                self.selected_node = None
        
        # Connect the event handlers
        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        fig.canvas.mpl_connect('button_release_event', on_release)
        
        # Create animation
        ani = FuncAnimation(fig, update, frames=len(steps)+1,
                          interval=1500, repeat=False)  # 1.5 seconds per step
        
        plt.show(block=False)
        return fig, ani
            
    def go_back(self):
        """Return to the graph menu"""
        # Clean up any existing plots
        if self.current_figure:
            plt.close(self.current_figure)
        if self.animation and self.animation.event_source:
            self.animation.event_source.stop()
        
        # Find and switch to graph menu
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break