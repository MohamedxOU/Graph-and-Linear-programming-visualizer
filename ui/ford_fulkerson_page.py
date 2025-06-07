import ast
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import ford_fulkerson

class FordFulkersonPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.current_figure = None
        self.paused = False
        self.current_frame = 0
        self.selected_node = None
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
        title = QLabel("Ford-Fulkerson Maximum Flow Algorithm")
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
        dict_layout.addWidget(QLabel("Enter flow network as dictionary (capacity):"))
        self.entry_graph = QTextEdit()
        self.entry_graph.setPlainText(
            "{\n"
            "    'S': {'A': 10, 'B': 5, 'C': 10},\n"
            "    'A': {'D': 8, 'B': 2},\n"
            "    'B': {'C': 9, 'E': 5},\n"
            "    'C': {'E': 4, 'T': 10},\n"
            "    'D': {'E': 6, 'T': 10},\n"
            "    'E': {'T': 10}\n"
            "}"
        )
        dict_layout.addWidget(self.entry_graph)
        dict_tab.setLayout(dict_layout)
        self.tabs.addTab(dict_tab, "Dictionary Input")

        # Table input tab
        table_tab = QWidget()
        table_layout = QVBoxLayout()
        table_layout.addWidget(QLabel("Enter flow network as adjacency list:"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["From", "To", "Capacity"])
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

        # Source and sink node inputs
        node_layout = QHBoxLayout()
        node_layout.addWidget(QLabel("Source Node:"))
        self.entry_source = QLineEdit("S")
        self.entry_source.setMaximumWidth(100)
        node_layout.addWidget(self.entry_source)
        
        node_layout.addWidget(QLabel("Sink Node:"))
        self.entry_sink = QLineEdit("T")
        self.entry_sink.setMaximumWidth(100)
        node_layout.addWidget(self.entry_sink)
        
        node_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(node_layout)

        # Control buttons
        control_layout = QHBoxLayout()
        self.btn_run = QPushButton("Find Maximum Flow")
        self.btn_run.clicked.connect(self.run_ford_fulkerson)
        self.btn_run.setObjectName("runButton")
        control_layout.addWidget(self.btn_run)
        main_layout.addLayout(control_layout)

        # Scrollable result display
        self.result_display = QTextEdit()
        self.result_display.setObjectName("resultDisplay")
        self.result_display.setReadOnly(True)
        self.result_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.result_display.setPlaceholderText("Maximum flow results will appear here...")
        main_layout.addWidget(self.result_display, stretch=1)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self):
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
            ("S", "A", 10), ("S", "B", 5), ("S", "C", 10),
            ("A", "D", 8), ("A", "B", 2),
            ("B", "C", 9), ("B", "E", 5),
            ("C", "E", 4), ("C", "T", 10),
            ("D", "E", 6), ("D", "T", 10),
            ("E", "T", 10)
        ]
        
        self.table.setRowCount(len(example_data))
        for row, (from_node, to_node, capacity) in enumerate(example_data):
            self.table.setItem(row, 0, QTableWidgetItem(from_node))
            self.table.setItem(row, 1, QTableWidgetItem(to_node))
            self.table.setItem(row, 2, QTableWidgetItem(str(capacity)))

    def add_table_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem("1"))  # Default capacity

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
                    
                self.entry_graph.setPlainText(content)
                self.tabs.setCurrentIndex(0)
                
                QMessageBox.information(
                    self,
                    "Import Successful",
                    "Flow network imported successfully!"
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
            from_item = self.table.item(row, 0)
            to_item = self.table.item(row, 1)
            capacity_item = self.table.item(row, 2)
            
            if from_item and to_item:
                from_node = from_item.text().strip()
                to_node = to_item.text().strip()
                try:
                    capacity = float(capacity_item.text()) if capacity_item else 1
                except ValueError:
                    capacity = 1
                
                if from_node and to_node:
                    if from_node not in graph:
                        graph[from_node] = {}
                    graph[from_node][to_node] = capacity
        return graph

    def run_ford_fulkerson(self):
        try:
            # Clean up any existing visualization
            self.cleanup_visualization()

            # Get graph from current tab
            if self.tabs.currentIndex() == 0:  # Dictionary tab
                graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            else:  # Table tab
                graph = self.get_graph_from_table()
            
            source = self.entry_source.text().strip()
            sink = self.entry_sink.text().strip()

            if not graph:
                QMessageBox.warning(self, "Error", "Flow network cannot be empty!")
                return
                
            if not source or not sink:
                QMessageBox.warning(self, "Error", "Please enter both source and sink nodes!")
                return
                
            if source not in graph or sink not in graph:
                QMessageBox.warning(self, "Error", "Source or sink node not in flow network!")
                return

            # Run Ford-Fulkerson algorithm
            max_flow, flow_network = ford_fulkerson(graph, source, sink)
            
            # Format results
            result_text = f"Maximum Flow from {source} to {sink}: {max_flow}\n\n"
            result_text += "Flow Network (flow/capacity):\n"
            result_text += "------------------------------\n"
            
            all_nodes = set(graph.keys())
            for neighbors in graph.values():
                all_nodes.update(neighbors.keys())
            
            for u in sorted(all_nodes):
                for v in sorted(all_nodes):
                    if u in graph and v in graph[u]:
                        capacity = graph[u][v]
                        flow = flow_network[u][v] if u in flow_network and v in flow_network[u] else 0
                        if flow > 0 or capacity > 0:
                            result_text += f"{u} → {v}: {flow}/{capacity}\n"
            
            self.result_display.setPlainText(result_text)
            self.result_display.ensureCursorVisible()
            
            # Show only the final result plot
            self.draw_ff_result_plot(graph, source, sink, max_flow, flow_network)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")
            self.result_display.setPlainText(f"Error: {str(e)}")
            self.cleanup_visualization()

    def draw_ff_result_plot(self, graph, source, sink, max_flow, flow_network):
        """Draw only the final result plot (no animation)"""
        try:
            self.cleanup_visualization()
            G = nx.DiGraph()
            for u in graph:
                for v in graph[u]:
                    G.add_edge(u, v, capacity=graph[u][v], flow=flow_network.get(u, {}).get(v, 0))
            self.G = G
            self.pos = nx.spring_layout(G)
            fig, ax = plt.subplots(figsize=(10, 8), tight_layout=True)
            self.current_figure = fig

            # Node colors
            node_colors = []
            for node in G.nodes():
                if node == source:
                    node_colors.append('green')
                elif node == sink:
                    node_colors.append('red')
                else:
                    node_colors.append('lightblue')

            # Edge colors and widths
            edge_colors = []
            edge_widths = []
            edge_labels = {}
            for u, v in G.edges():
                flow = flow_network.get(u, {}).get(v, 0)
                if flow > 0:
                    edge_colors.append('blue')
                    edge_widths.append(3)
                else:
                    edge_colors.append('gray')
                    edge_widths.append(1)
                edge_labels[(u, v)] = f"{flow}/{graph[u][v]}"

            nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
            nx.draw_networkx_labels(G, self.pos, ax=ax, font_size=10)
            nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, 
                                   width=edge_widths, arrows=True, arrowstyle='->', arrowsize=15)
            nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels, font_size=8)
            ax.set_title(f"Maximum Flow: {max_flow}\nFlow shown as flow/capacity", fontsize=12)
            ax.axis('off')
            fig.canvas.manager.set_window_title('Ford-Fulkerson Result')
            plt.show(block=False)
        except Exception as e:
            QMessageBox.critical(self, "Visualization Error", f"Failed to create result plot: {str(e)}")
            self.cleanup_visualization()

    def cleanup_visualization(self):
        """Clean up any existing visualization resources"""
        if hasattr(self, 'current_figure') and self.current_figure:
            try:
                plt.close(self.current_figure)
            except:
                pass
            self.current_figure = None

    def go_back(self):
        """Return to the graph menu"""
        self.cleanup_visualization()
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break