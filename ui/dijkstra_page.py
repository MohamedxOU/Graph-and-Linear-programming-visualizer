import ast
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import dijkstra

class DijkstraPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
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

        # File import button
        import_layout = QHBoxLayout()
        self.btn_import = QPushButton("Import Graph from File")
        self.btn_import.clicked.connect(self.import_from_file)
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
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Shortest path will appear here...")
        main_layout.addWidget(self.result_display)

        self.setLayout(main_layout)

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
        self.table.setItem(row, 2, QTableWidgetItem("1"))

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
            if self.tabs.currentIndex() == 0:
                graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            else:
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
                self.result_display.setPlainText(f"No path exists from {start} to {end}!")
                return

            path = self.reconstruct_path(previous_nodes, start, end)
            total_distance = distances[end]

            result_text = f"Shortest path from {start} to {end}:\n"
            result_text += " → ".join(path) + "\n"
            result_text += f"Total distance: {total_distance}"
            self.result_display.setPlainText(result_text)

            # Visualization: animate if < 15 nodes, else static
            if len(graph) < 15:
                self.current_figure, self.animation = self.dijkstra_visualizer(graph, start, end, distances, previous_nodes)
            else:
                self.current_figure = self.dijkstra_static_plot(graph, start, end, distances, previous_nodes)
                self.animation = None

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def reconstruct_path(self, previous_nodes, start, end):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        if path[0] != start:
            return []
        return path

    def dijkstra_static_plot(self, graph, start, end, distances, previous_nodes):
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        self.pos = nx.spring_layout(G)
        self.G = G
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig

        path = self.reconstruct_path(previous_nodes, start, end)
        path_edges = list(zip(path[:-1], path[1:]))

        node_colors = []
        for node in G.nodes():
            if node in path:
                node_colors.append('lightblue')
            else:
                node_colors.append('lightgray')

        edge_colors = []
        edge_widths = []
        for edge in G.edges():
            if edge in path_edges or (edge[1], edge[0]) in path_edges:
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
        ax.set_title(f"Shortest path from {start} to {end}: {distances[end]}")
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
            ax.set_title(f"Shortest path from {start} to {end}: {distances[end]}")
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

    def dijkstra_visualizer(self, graph, start, end, distances, previous_nodes):
        import heapq
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        self.pos = nx.spring_layout(G)
        self.G = G
        self.current_frame = 0

        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig

        path = self.reconstruct_path(previous_nodes, start, end)
        visited_order = []
        priority_queue = [(0, start)]
        visited = set()
        steps = []
        local_distances = dict(distances)
        local_previous = dict(previous_nodes)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node in visited:
                continue
            visited.add(current_node)
            visited_order.append(current_node)
            steps.append((current_node, dict(local_distances), dict(local_previous)))
            for neighbor, weight in graph.get(current_node, {}).items():
                distance = current_distance + weight
                if distance < local_distances[neighbor]:
                    local_distances[neighbor] = distance
                    local_previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        def update(frame):
            self.current_frame = frame
            ax.clear()
            if frame < len(steps):
                current_node, current_distances, current_previous = steps[frame]
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node == current_node:
                        node_colors.append('red')
                    elif node in visited_order[:frame]:
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')
                    dist = current_distances.get(node, float('inf'))
                    node_labels[node] = f"{node}\n({dist if dist != float('inf') else '∞'})"
                edge_colors = []
                edge_labels = {}
                for u, v, data in G.edges(data=True):
                    if u == current_node and v in graph[current_node]:
                        edge_colors.append('red')
                    else:
                        edge_colors.append('gray')
                    edge_labels[(u, v)] = str(data['weight'])
                path_edges = []
                for node in visited_order[:frame+1]:
                    if current_previous[node] is not None:
                        path_edges.append((current_previous[node], node))
                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, labels=node_labels, font_size=10)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=2)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edgelist=path_edges, edge_color='blue', width=3)
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                ax.set_title(f"Step {frame+1}/{len(steps)}: Visiting {current_node}\n"
                           f"Current distance to {end}: {current_distances.get(end, float('inf'))}")
            else:
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
                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, labels=node_labels, font_size=10)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color='gray', width=1)
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G, self.pos, ax=ax, edgelist=path_edges, edge_color='blue', width=3)
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                ax.set_title(f"Shortest path found!\n{start} to {end}: {distances[end]}")
            ax.axis('off')

        self.update = update

        # Mouse event handlers for dragging nodes
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
        for index in range(self.stack.count()):
            widget = self.stack.widget(index)
            if widget.__class__.__name__ == "GraphMenu":
                self.stack.setCurrentWidget(widget)
                break