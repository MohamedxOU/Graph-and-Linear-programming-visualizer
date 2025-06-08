import ast
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import prim
import heapq

class PrimPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.current_figure = None
        self.animation = None
        self.paused = False
        self.selected_node = None
        self.offset = (0, 0)
        self.current_frame = 0
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
        title = QLabel("Prim's Minimum Spanning Tree Algorithm")
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
            "    'A': {'B': 2, 'D': 6},\n"
            "    'B': {'A': 2, 'C': 3, 'D': 8, 'E': 5},\n"
            "    'C': {'B': 3, 'E': 7},\n"
            "    'D': {'A': 6, 'B': 8, 'E': 9},\n"
            "    'E': {'B': 5, 'C': 7, 'D': 9}\n"
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

        # Start node input
        node_layout = QHBoxLayout()
        node_layout.addWidget(QLabel("Start Node:"))
        self.entry_start = QLineEdit("A")
        self.entry_start.setMaximumWidth(100)
        node_layout.addWidget(self.entry_start)
        node_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(node_layout)

        # Control buttons
        control_layout = QHBoxLayout()
        self.btn_run = QPushButton("Find Minimum Spanning Tree")
        self.btn_run.clicked.connect(self.run_prim)
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
        self.result_display.setPlaceholderText("Minimum spanning tree will appear here...")
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
            ("A", "B", 2),
            ("A", "D", 6),
            ("B", "C", 3),
            ("B", "D", 8),
            ("B", "E", 5),
            ("C", "E", 7),
            ("D", "E", 9)
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
                    if neighbor not in graph:
                        graph[neighbor] = {}
                    graph[node][neighbor] = weight
                    graph[neighbor][node] = weight  # Undirected graph
        return graph

    def run_prim(self):
        try:
            # Get graph from current tab
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            else:  # Table tab
                graph = self.get_graph_from_table()
            
            start = self.entry_start.text().strip()

            if not graph:
                QMessageBox.warning(self, "Error", "Graph cannot be empty!")
                return
                
            if not start:
                QMessageBox.warning(self, "Error", "Please enter a start node!")
                return
                
            if start not in graph:
                QMessageBox.warning(self, "Error", "Start node not in graph!")
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

            # Run Prim's algorithm
            mst = prim(graph, start)
            
            # Calculate total weight
            total_weight = sum(weight for neighbors in mst.values() for weight in neighbors.values()) // 2
            
            # Format results with aligned columns
            result_text = "Minimum Spanning Tree Edges:\n"
            result_text += "---------------------------\n"
            edges = set()
            for u in sorted(mst.keys()):
                for v in sorted(mst[u].keys()):
                    if (v, u) not in edges:  # Avoid duplicate edges
                        edges.add((u, v))
                        result_text += f"{u:>2} —— {v:<2} (weight: {mst[u][v]:<4})\n"
            
            result_text += "---------------------------\n"
            result_text += f"Total weight: {total_weight}\n"
            result_text += f"Total edges: {len(edges)}"
            
            # Display in scrollable area
            self.result_display.setPlainText(result_text)
            self.result_display.ensureCursorVisible()  # Auto-scroll to bottom
            
            # Visualization: animate if < 15 nodes, else static
            if len(graph) < 15:
                self.current_figure, self.animation = self.prim_visualizer(graph, mst, start)
            else:
                self.btn_pause.setEnabled(False)
                self.current_figure = self.prim_static_plot(graph, mst, start)
                self.animation = None

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")
            self.result_display.setPlainText(f"Error: {str(e)}")

    def prim_static_plot(self, graph, mst, start):
        """Show static MST result with draggable nodes for large graphs"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        self.pos = nx.spring_layout(G)
        self.G = G
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig

        # Prepare MST edges
        mst_edges = set()
        for u in mst:
            for v in mst[u]:
                mst_edges.add((u, v))
                mst_edges.add((v, u))

        # Node colors
        node_colors = []
        for node in G.nodes():
            if node == start:
                node_colors.append('red')
            elif node in mst:
                node_colors.append('lightgreen')
            else:
                node_colors.append('lightgray')

        # Edge colors and widths
        edge_colors = []
        edge_widths = []
        for edge in G.edges():
            if edge in mst_edges or (edge[1], edge[0]) in mst_edges:
                edge_colors.append('blue')
                edge_widths.append(3)
            else:
                edge_colors.append('gray')
                edge_widths.append(1)

        nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
        nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
        nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
        edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
        ax.set_title("Minimum Spanning Tree (static view)")
        ax.axis('off')

        # Mouse event handlers for dragging nodes
        def on_press(event):
            if event.inaxes != ax:
                return
            for node in G.nodes():
                x, y = self.pos[node]
                if (x - event.xdata) ** 2 + (y - event.ydata) ** 2 < 0.01:
                    self.selected_node = node
                    self.offset = (x - event.xdata, y - event.ydata)
                    break

        def on_motion(event):
            if not hasattr(self, 'selected_node') or self.selected_node is None or event.inaxes != ax:
                return
            self.pos[self.selected_node] = (event.xdata + self.offset[0], event.ydata + self.offset[1])
            ax.clear()
            nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
            nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
            nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
            nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
            ax.set_title("Minimum Spanning Tree (static view)")
            ax.axis('off')
            fig.canvas.draw_idle()

        def on_release(event):
            if hasattr(self, 'selected_node'):
                self.selected_node = None

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        fig.canvas.mpl_connect('button_release_event', on_release)

        plt.show(block=False)
        return fig

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
            G = nx.Graph()
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            else:  # Table tab
                graph = self.get_graph_from_table()
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)
            self.pos = nx.spring_layout(G)
            if hasattr(self, 'update'):
                self.update(self.current_frame)
                self.current_figure.canvas.draw_idle()
            else:
                # For static plot
                ax = self.current_figure.axes[0]
                # Reuse last MST if possible, else just draw all edges
                node_colors = ['lightgreen' for _ in G.nodes()]
                edge_colors = ['blue' for _ in G.edges()]
                edge_widths = [3 for _ in G.edges()]
                ax.clear()
                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                ax.set_title("Minimum Spanning Tree (static view)")
                ax.axis('off')
                self.current_figure.canvas.draw_idle()

    def prim_visualizer(self, graph, mst, start):
        """Visualize Prim's algorithm with step-by-step animation and draggable nodes"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        
        self.pos = nx.spring_layout(G)
        self.G = G
        self.current_frame = 0
        
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig
        
        # Reconstruct the steps of Prim's algorithm
        visited = set([start])
        edges = [
            (weight, start, neighbor)
            for neighbor, weight in graph[start].items()
        ]
        heapq.heapify(edges)
        
        steps = []
        mst_edges = set()
        
        while edges:
            weight, u, v = heapq.heappop(edges)
            if v not in visited:
                visited.add(v)
                mst_edges.add((u, v))
                mst_edges.add((v, u))  # For undirected graph
                
                steps.append((u, v, weight, visited.copy(), mst_edges.copy()))
                
                for neighbor, edge_weight in graph[v].items():
                    if neighbor not in visited:
                        heapq.heappush(edges, (edge_weight, v, neighbor))
        
        def update(frame):
            self.current_frame = frame
            ax.clear()
            
            if frame < len(steps):
                u, v, weight, current_visited, current_mst_edges = steps[frame]
                
                node_colors = []
                for node in G.nodes():
                    if node == u or node == v:
                        node_colors.append('red')
                    elif node in current_visited:
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')
                
                edge_colors = []
                edge_widths = []
                for edge in G.edges():
                    if edge in current_mst_edges or (edge[1], edge[0]) in current_mst_edges:
                        edge_colors.append('blue')
                        edge_widths.append(3)
                    elif edge[0] in [u, v] and edge[1] in [u, v]:
                        edge_colors.append('red')
                        edge_widths.append(3)
                    else:
                        edge_colors.append('gray')
                        edge_widths.append(1)
                
                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                ax.set_title(f"Step {frame+1}/{len(steps)}: Adding edge {u}-{v} (weight: {weight})\n"
                           f"Visited nodes: {', '.join(sorted(current_visited))}")
            else:
                node_colors = ['lightgreen' for _ in G.nodes()]
                edge_colors = ['blue' if edge in mst_edges or (edge[1], edge[0]) in mst_edges else 'gray' 
                             for edge in G.edges()]
                edge_widths = [3 if edge in mst_edges or (edge[1], edge[0]) in mst_edges else 1 
                             for edge in G.edges()]
                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=edge_widths)
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                total_weight = sum(d['weight'] for u, v, d in G.edges(data=True) 
                                 if (u, v) in mst_edges or (v, u) in mst_edges) // 2
                ax.set_title(f"Minimum Spanning Tree Complete!\nTotal weight: {total_weight}")
            ax.axis('off')
        
        self.update = update

        # Mouse event handlers for dragging nodes (always enabled)
        def on_press(event):
            if event.inaxes != ax:
                return
            for node in G.nodes():
                x, y = self.pos[node]
                if (x - event.xdata)**2 + (y - event.ydata)**2 < 0.01:
                    self.selected_node = node
                    self.offset = (x - event.xdata, y - event.ydata)
                    break

        def on_motion(event):
            if not hasattr(self, 'selected_node') or self.selected_node is None or event.inaxes != ax:
                return
            self.pos[self.selected_node] = (event.xdata + self.offset[0], event.ydata + self.offset[1])
            update(self.current_frame)
            fig.canvas.draw_idle()

        def on_release(event):
            if hasattr(self, 'selected_node'):
                self.selected_node = None

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        fig.canvas.mpl_connect('button_release_event', on_release)
        
        ani = FuncAnimation(fig, update, frames=len(steps)+1,
                          interval=1500, repeat=False)
        
        plt.show(block=False)
        return fig, ani

    def go_back(self):
        """Return to the graph menu"""
        if self.current_figure:
            plt.close(self.current_figure)
        if self.animation and self.animation.event_source:
            self.animation.event_source.stop()
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break