import ast
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTabWidget,
    QSpacerItem, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt
from algorithms.graph_algos import a_star, reconstruct_path_as

class AStarPage(QWidget):
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
        title = QLabel("A* Pathfinding Algorithm")
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

        # Graph dictionary tab
        graph_tab = QWidget()
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(QLabel("Enter graph (weighted):"))
        self.entry_graph = QTextEdit()
        self.entry_graph.setPlainText(
            "{\n"
            "    'A': {'B': 1, 'C': 3},\n"
            "    'B': {'A': 1, 'D': 5, 'E': 2},\n"
            "    'C': {'A': 3, 'F': 2},\n"
            "    'D': {'B': 5, 'H': 1},\n"
            "    'E': {'B': 2, 'H': 4},\n"
            "    'F': {'C': 2, 'G': 1},\n"
            "    'G': {'F': 1, 'H': 2},\n"
            "    'H': {'D': 1, 'E': 4, 'G': 2}\n"
            "}"
        )
        graph_layout.addWidget(self.entry_graph)
        graph_tab.setLayout(graph_layout)
        self.tabs.addTab(graph_tab, "Graph Input")

        # Heuristic input tab
        heuristic_tab = QWidget()
        heuristic_layout = QVBoxLayout()
        heuristic_layout.addWidget(QLabel("Enter heuristic values (straight-line distance to end):"))
        self.entry_heuristic = QTextEdit()
        self.entry_heuristic.setPlainText(
            "{\n"
            "    'A': 5,\n"
            "    'B': 4,\n"
            "    'C': 3,\n"
            "    'D': 2,\n"
            "    'E': 3,\n"
            "    'F': 2,\n"
            "    'G': 1,\n"
            "    'H': 0\n"
            "}"
        )
        heuristic_layout.addWidget(self.entry_heuristic)
        heuristic_tab.setLayout(heuristic_layout)
        self.tabs.addTab(heuristic_tab, "Heuristic Values")
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
        self.btn_run = QPushButton("Find Path (A*)")
        self.btn_run.clicked.connect(self.run_astar)
        main_layout.addWidget(self.btn_run)

        # Result display
        self.label_result = QLabel("Path will appear here...")
        self.label_result.setWordWrap(True)
        main_layout.addWidget(self.label_result)

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

    def run_astar(self):
        try:
            graph = ast.literal_eval(self.entry_graph.toPlainText().strip())
            heuristic = ast.literal_eval(self.entry_heuristic.toPlainText().strip())
            start = self.entry_start.text().strip()
            end = self.entry_end.text().strip()

            if not graph or not heuristic:
                QMessageBox.warning(self, "Error", "Graph and heuristic cannot be empty!")
                return
            if start not in graph or end not in graph:
                QMessageBox.warning(self, "Error", "Start or end node not in graph!")
                return

            # Run A* algorithm
            path = a_star(graph, start, end, heuristic)

            if not path:
                self.label_result.setText(f"No path found from {start} to {end}!")
                return

            # Close previous visualization if exists
            if self.current_figure:
                plt.close(self.current_figure)
            if self.animation and self.animation.event_source:
                self.animation.event_source.stop()

            total_cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            result_text = f"A* Path from {start} to {end}:\n"
            result_text += " → ".join(path) + "\n"
            result_text += f"Total cost: {total_cost}"
            self.label_result.setText(result_text)

            # Visualization: animate if < 15 nodes, else static
            if len(graph) < 15:
                self.current_figure, self.animation = self.astar_visualizer(
                    graph, heuristic, start, end, path
                )
            else:
                self.current_figure = self.astar_static_plot(
                    graph, heuristic, start, end, path
                )
                self.animation = None

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def astar_static_plot(self, graph, heuristic, start, end, final_path):
        """Show static A* result with draggable nodes for large graphs"""
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        self.pos = nx.spring_layout(G)
        self.G = G
        fig, ax = plt.subplots(figsize=(10, 8))
        self.current_figure = fig

        path_edges = list(zip(final_path[:-1], final_path[1:]))

        node_colors = []
        for node in G.nodes():
            if node in final_path:
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
        ax.set_title(f"A* Path from {start} to {end}: {sum(graph[final_path[i]][final_path[i+1]] for i in range(len(final_path)-1))}")
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
            ax.set_title(f"A* Path from {start} to {end}: {sum(graph[final_path[i]][final_path[i+1]] for i in range(len(final_path)-1))}")
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

    def astar_visualizer(self, graph, heuristic, start, end, final_path):
        """Visualize A* algorithm with step-by-step animation and draggable nodes"""
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

        # Reconstruct the exploration steps
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in graph}
        g_score[start] = 0
        f_score = {node: float('inf') for node in graph}
        f_score[start] = heuristic[start]
        open_set_hash = {start}

        steps = []
        visited_order = []

        while open_set:
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            visited_order.append(current)

            # Save current state for animation
            steps.append({
                'current': current,
                'open_set': open_set.copy(),
                'came_from': came_from.copy(),
                'g_score': g_score.copy(),
                'f_score': f_score.copy()
            })

            if current == end:
                break

            for neighbor, cost in graph[current].items():
                tentative_g_score = g_score[current] + cost

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

        def update(frame):
            self.current_frame = frame
            ax.clear()

            if frame < len(steps):
                state = steps[frame]
                current_node = state['current']

                # Prepare node colors and labels
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node == current_node:
                        node_colors.append('red')
                    elif node in [n[1] for n in state['open_set']]:
                        node_colors.append('lightyellow')
                    elif node in visited_order[:frame]:
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')

                    g = state['g_score'].get(node, float('inf'))
                    f = state['f_score'].get(node, float('inf'))
                    node_labels[node] = f"{node}\ng={g if g != float('inf') else '∞'}\nf={f if f != float('inf') else '∞'}"

                edge_colors = []
                edge_labels = {}
                for u, v, data in G.edges(data=True):
                    if u == current_node and v in graph[current_node]:
                        edge_colors.append('red')
                    else:
                        edge_colors.append('gray')
                    edge_labels[(u, v)] = str(data['weight'])

                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, labels=node_labels, font_size=8)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color=edge_colors, width=2)
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)

                ax.set_title(f"Step {frame+1}/{len(steps)}: Visiting {current_node}\n"
                           f"Current f-score: {state['f_score'].get(current_node, float('inf'))}")
            else:
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node in final_path:
                        node_colors.append('lightblue')
                    elif node in visited_order:
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')

                    g = steps[-1]['g_score'].get(node, float('inf'))
                    f = steps[-1]['f_score'].get(node, float('inf'))
                    node_labels[node] = f"{node}\ng={g if g != float('inf') else '∞'}\nf={f if f != float('inf') else '∞'}"

                nx.draw_networkx_nodes(G, self.pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, self.pos, ax=ax, labels=node_labels, font_size=8)
                nx.draw_networkx_edges(G, self.pos, ax=ax, edge_color='gray', width=1)
                path_edges = list(zip(final_path[:-1], final_path[1:]))
                nx.draw_networkx_edges(G, self.pos, ax=ax, edgelist=path_edges, edge_color='blue', width=3)
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, self.pos, ax=ax, edge_labels=edge_labels)
                total_cost = sum(graph[final_path[i]][final_path[i+1]] for i in range(len(final_path)-1))
                ax.set_title(f"Path found!\n{start} to {end}: Cost = {total_cost}")

            ax.axis('off')

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