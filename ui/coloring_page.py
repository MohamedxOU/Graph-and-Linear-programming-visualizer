import ast
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import coloration_glouton

class ColoringPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.current_figure = None
        self.animation = None
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
        title = QLabel("Greedy Graph Coloring Algorithm")
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

        # Run button
        self.button_run_coloring = QPushButton("Run Greedy Coloring")
        self.button_run_coloring.clicked.connect(self.run_coloring)
        self.button_run_coloring.setObjectName("runButton")
        main_layout.addWidget(self.button_run_coloring)

        # Result display with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        result_container = QWidget()
        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(0)
        self.label_result = QLabel("Coloring result will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label_result.setObjectName("resultLabel")
        result_layout.addWidget(self.label_result)
        result_container.setLayout(result_layout)
        scroll_area.setWidget(result_container)
        scroll_area.setMinimumHeight(100)
        scroll_area.setMaximumHeight(250)
        main_layout.addWidget(scroll_area)

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
            #importButton {
                background-color: #D08770;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            #importButton:hover {
                background-color: #EBCB8B;
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

    def run_coloring(self):
        try:
            # Get graph from current tab
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graphe = ast.literal_eval(self.entry_graphe.toPlainText().strip())
            else:  # Table tab
                graphe = self.get_graph_from_table()

            if not graphe:
                QMessageBox.warning(self, "Error", "Graph cannot be empty!")
                return
            
            # Close previous visualization if exists
            if self.current_figure:
                plt.close(self.current_figure)
            if self.animation and self.animation.event_source:
                self.animation.event_source.stop()
            
            # Run coloring and get the result
            coloriage = coloration_glouton(graphe)
            result_text = "Coloring Result:\n"
            for node, color in coloriage.items():
                result_text += f"Node {node}: Color {color}\n"
            self.label_result.setText(result_text)
            
            # Only animate if number of nodes < 15
            if len(graphe) < 15:
                self.current_figure, self.animation = self.color_visualizer(graphe, coloriage)
            else:
                self.current_figure = self.color_static_plot(graphe, coloriage)
                self.animation = None

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def color_static_plot(self, graph, coloring):
        """Show static coloring result with draggable nodes for large graphs"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        self.pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig

        color_values = list(coloring.values())
        max_color = max(color_values) if color_values else 1
        cmap = plt.cm.get_cmap('tab20', max_color)

        node_colors = []
        node_labels = {}
        for node in G.nodes():
            if node in coloring:
                color_idx = coloring[node] - 1
                node_colors.append(cmap(color_idx / max_color))
                node_labels[node] = f"{node}\n(Color {coloring[node]})"
            else:
                node_colors.append('lightgray')
                node_labels[node] = node

        nx.draw(G, self.pos, ax=ax, with_labels=True, labels=node_labels,
                node_color=node_colors, edge_color='gray',
                width=2, font_size=10, font_weight='bold')
        ax.set_title("Greedy Coloring Result")
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
            nx.draw(G, self.pos, ax=ax, with_labels=True, labels=node_labels,
                    node_color=node_colors, edge_color='gray',
                    width=2, font_size=10, font_weight='bold')
            ax.set_title("Greedy Coloring Result")
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

    def color_visualizer(self, graph, coloring):
        """Visualize graph coloring with step-by-step animation and draggable nodes"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        
        self.pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(10, 8))
        colored_order = list(coloring.keys())
        color_values = list(coloring.values())
        max_color = max(color_values) if color_values else 1
        cmap = plt.cm.get_cmap('tab20', max_color)

        def update(frame):
            ax.clear()
            node_colors = []
            node_labels = {}
            current_node = colored_order[frame] if frame < len(colored_order) else None
            for node in G.nodes():
                if node in colored_order[:frame+1]:
                    color_idx = coloring[node] - 1
                    node_colors.append(cmap(color_idx / max_color))
                    node_labels[node] = f"{node}\n(Color {coloring[node]})"
                else:
                    node_colors.append('lightgray')
                    node_labels[node] = node
            if current_node:
                nx.draw_networkx_nodes(G, self.pos, nodelist=[current_node],
                                      node_color='red', ax=ax, node_size=1000)
            nx.draw(G, self.pos, ax=ax, with_labels=True, labels=node_labels,
                   node_color=node_colors, edge_color='gray',
                   width=2, font_size=10, font_weight='bold')
            info_text = f"Step {frame+1}/{len(colored_order)}: "
            if current_node:
                info_text += f"Coloring node {current_node} with color {coloring[current_node]}"
            else:
                info_text += "Coloring complete"
            ax.set_title(info_text)
            ax.axis('off')

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
            update(self.current_frame)
            fig.canvas.draw_idle()

        def on_release(event):
            if hasattr(self, 'selected_node'):
                self.selected_node = None

        self.current_frame = 0
        self.update = update

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        fig.canvas.mpl_connect('button_release_event', on_release)

        ani = FuncAnimation(fig, update, frames=len(colored_order)+1,
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