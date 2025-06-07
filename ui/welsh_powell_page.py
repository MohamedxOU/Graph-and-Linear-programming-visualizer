import ast
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import welsh_powell

class WelshPowellPage(QWidget):
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

        # Back button row
        back_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to Graph Menu")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setObjectName("backButton")
        back_layout.addWidget(self.btn_back)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("Welsh-Powell Graph Coloring Algorithm")
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
            "    'A': ['B', 'C', 'D'],\n"
            "    'B': ['A', 'C'],\n"
            "    'C': ['A', 'B', 'D'],\n"
            "    'D': ['A', 'C', 'E'],\n"
            "    'E': ['D', 'F', 'G'],\n"
            "    'F': ['E', 'G'],\n"
            "    'G': ['E', 'F', 'H'],\n"
            "    'H': ['G']\n"
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
        self.button_run_coloring = QPushButton("Run Welsh-Powell Coloring")
        self.button_run_coloring.clicked.connect(self.run_coloring)
        self.button_run_coloring.setObjectName("runButton")
        main_layout.addWidget(self.button_run_coloring)

        # Result display
        self.label_result = QLabel("Coloring result will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setObjectName("resultLabel")
        main_layout.addWidget(self.label_result)

        self.setLayout(main_layout)
        
        # Apply styling (same as before)
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
        """Load example data into the table"""
        example_data = [
            ("A", "B, C, D"),
            ("B", "A, C"),
            ("C", "A, B, D"),
            ("D", "A, C, E"),
            ("E", "D, F, G"),
            ("F", "E, G"),
            ("G", "E, F, H"),
            ("H", "G")
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
            coloriage = welsh_powell(graphe)
            result_text = "Coloring Result:\n"
            for node, color in coloriage.items():
                result_text += f"Node {node}: Color {color}\n"
            
            self.label_result.setText(result_text)
            
            # Create visualization
            self.current_figure, self.animation = self.color_visualizer(graphe, coloriage)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def color_visualizer(self, graph, coloring):
        """Visualize graph coloring with step-by-step animation"""
        # Create the graph structure
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get nodes sorted by degree (as in the algorithm)
        nodes_sorted = sorted(graph.keys(), key=lambda x: -len(graph[x]))
        max_color = max(coloring.values()) if coloring.values() else 1
        
        # Create a colormap with enough distinct colors
        cmap = plt.cm.get_cmap('tab20', max_color)
        
        # Animation update function
        def update(frame):
            ax.clear()
            
            # Prepare node colors and labels
            node_colors = []
            node_labels = {}
            current_color_group = []
            
            for i, node in enumerate(nodes_sorted):
                if coloring[node] <= frame + 1:
                    color_idx = coloring[node] - 1  # Convert to 0-based index
                    node_colors.append(cmap(color_idx/max_color))
                    node_labels[node] = f"{node}\n(Color {coloring[node]})"
                    
                    # Track nodes being colored in this step
                    if coloring[node] == frame + 1:
                        current_color_group.append(node)
                else:
                    node_colors.append('lightgray')
                    node_labels[node] = node
            
            # Highlight nodes being colored in this step
            if current_color_group:
                nx.draw_networkx_nodes(G, pos, nodelist=current_color_group, 
                                     node_color='red', ax=ax, node_size=1000)
            
            # Draw the graph
            nx.draw(G, pos, ax=ax, with_labels=True, labels=node_labels,
                   node_color=node_colors, edge_color='gray',
                   width=2, font_size=10, font_weight='bold')
            
            # Add color information
            info_text = f"Step {frame+1}/{max_color}: "
            if current_color_group:
                info_text += f"Applying color {frame+1} to nodes: {', '.join(current_color_group)}"
            else:
                info_text += "Coloring complete"
            
            ax.set_title(info_text)
            ax.axis('off')
        
        # Create animation
        ani = FuncAnimation(fig, update, frames=max_color,
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