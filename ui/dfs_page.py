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
from algorithms.graph_algos import dfs

class DFSPage(QWidget):
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

        # Back button row
        back_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to Graph Menu")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        back_layout.addWidget(self.btn_back)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Depth-First Search (DFS) Algorithm")
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
        self.button_run_dfs = QPushButton("Run DFS Algorithm")
        self.button_run_dfs.clicked.connect(self.run_dfs)
        self.button_run_dfs.setObjectName("runButton")
        main_layout.addWidget(self.button_run_dfs)

        # Result display
        self.label_result = QLabel("DFS traversal will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setObjectName("resultLabel")
        main_layout.addWidget(self.label_result)

        self.setLayout(main_layout)
        
        # Apply styling (same as BFS page)
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
            #importButton {
                background-color: #D08770;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            #importButton:hover {
                background-color: #EBCB8B;
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
                background-color: #88C0D0;
                color: #2E3440;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            #runButton:hover {
                background-color: #8FBCBB;
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
            try:
                graph_dict = ast.literal_eval(content)
                if not isinstance(graph_dict, dict):
                    raise ValueError("File content must be a dictionary")
                self.entry_graphe.setPlainText(content)
                self.tabs.setCurrentIndex(0)
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

    def run_dfs(self):
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
            
            # Run DFS and get the traversal order
            traversal_order = dfs(graphe, noeud_depart)
            self.label_result.setText(f"DFS Traversal Order:\n{' → '.join(traversal_order)}")
            
            # Close previous visualization if exists
            if self.current_figure:
                plt.close(self.current_figure)
            if self.animation and self.animation.event_source:
                self.animation.event_source.stop()

            # Only animate if number of nodes < 15
            if len(graphe) < 15:
                self.paused = False
                self.current_figure, self.animation = self.dfs_visualizer(graphe, noeud_depart)
            else:
                self.current_figure = self.dfs_static_plot(graphe, noeud_depart)
                self.animation = None

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def dfs_static_plot(self, graph, start_node):
        """Show static DFS result with draggable nodes for large graphs"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        self.pos = nx.spring_layout(G)
        self.G = G
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig

        traversal_order = dfs(graph, start_node)
        node_colors = []
        for node in G.nodes():
            if node == start_node:
                node_colors.append('red')
            elif node in traversal_order:
                idx = traversal_order.index(node)
                shade = 0.3 + 0.7 * (idx / len(traversal_order))
                node_colors.append((0.0, 0.0, shade, 1.0))
            else:
                node_colors.append('lightgray')

        nx.draw(G, self.pos, ax=ax, with_labels=True,
                node_color=node_colors, edge_color='gray',
                width=2, node_size=800, font_size=12, font_weight='bold')
        ax.set_title(f"DFS Traversal: {' → '.join(traversal_order)}")

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
            nx.draw(G, self.pos, ax=ax, with_labels=True,
                    node_color=node_colors, edge_color='gray',
                    width=2, node_size=800, font_size=12, font_weight='bold')
            ax.set_title(f"DFS Traversal: {' → '.join(traversal_order)}")
            fig.canvas.draw_idle()

        def on_release(event):
            if hasattr(self, 'selected_node'):
                self.selected_node = None

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        fig.canvas.mpl_connect('button_release_event', on_release)

        plt.show(block=False)
        return fig

    def dfs_visualizer(self, graph, start_node):
        """Visualize DFS traversal with step-by-step animation and draggable nodes"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        
        self.pos = nx.spring_layout(G)
        self.G = G
        self.current_frame = 0
        
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig
        
        traversal_order = dfs(graph, start_node)
        self.traversal_order = traversal_order

        def update(frame):
            self.current_frame = frame
            ax.clear()
            current_node = traversal_order[frame]
            
            node_colors = []
            for node in G.nodes():
                if node == current_node:
                    node_colors.append('red')
                elif node in traversal_order[:frame]:
                    idx = traversal_order.index(node)
                    shade = 0.3 + 0.7 * (idx / len(traversal_order))
                    node_colors.append((0.0, 0.0, shade, 1.0))
                else:
                    node_colors.append('lightgray')
            
            path_edges = []
            for i in range(1, frame+1):
                if traversal_order[i-1] in graph.get(traversal_order[i], []):
                    path_edges.append((traversal_order[i-1], traversal_order[i]))
                elif traversal_order[i] in graph.get(traversal_order[i-1], []):
                    path_edges.append((traversal_order[i], traversal_order[i-1]))
            
            edge_colors = []
            for edge in G.edges():
                if edge in path_edges or tuple(reversed(edge)) in path_edges:
                    edge_colors.append('red')
                else:
                    edge_colors.append('gray')
            
            nx.draw(G, self.pos, ax=ax, with_labels=True,
                   node_color=node_colors, edge_color=edge_colors,
                   width=2, node_size=800, font_size=12, font_weight='bold')
            
            ax.set_title(f"DFS Step {frame+1}/{len(traversal_order)}: Visiting {current_node}\n"
                        f"Traversal: {' → '.join(traversal_order[:frame+1])}")

        self.update = update

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
        
        ani = FuncAnimation(fig, update, frames=len(traversal_order),
                          interval=1000, repeat=False)
        
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