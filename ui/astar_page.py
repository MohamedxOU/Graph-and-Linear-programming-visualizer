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
from algorithms.graph_algos import a_star, reconstruct_path_as
import heapq

class AStarPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.graph = {}
        self.heuristic = {}
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
        self.btn_back.setObjectName("backButton")
        back_layout.addWidget(self.btn_back)
        main_layout.addLayout(back_layout)

        # Title
        title = QLabel("A* Pathfinding Algorithm")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

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
        self.btn_run.setObjectName("runButton")
        main_layout.addWidget(self.btn_run)

        # Result display
        self.label_result = QLabel("Path will appear here...")
        self.label_result.setWordWrap(True)
        self.label_result.setObjectName("resultLabel")
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
            QTextEdit, QLineEdit {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                font-family: monospace;
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
            #resultLabel {
                font-size: 16px;
                padding: 15px;
                background-color: #3B4252;
                border-radius: 8px;
                min-height: 60px;
            }
        """)

    def run_astar(self):
        try:
 

            # Get inputs
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
            
            # Update result immediately
            self.label_result.setText(result_text)
            
            # Create visualization
            self.current_figure, self.animation = self.astar_visualizer(
                graph, heuristic, start, end, path
            )
            
            plt.show()  # <- Add this to ensure the figure window stays open


        except Exception as e:
            QMessageBox.critical(self, "Error", f"Input error: {str(e)}")

    def astar_visualizer(self, graph, heuristic, start, end, final_path):
        """Visualize A* algorithm with step-by-step animation"""
        # Create the graph structure
        G = nx.DiGraph() if nx.is_directed(nx.DiGraph(graph)) else nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Reconstruct the exploration steps
        open_set = []
        heapq.heappush(open_set, (heuristic[start], start))
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
        
        # Animation update function
        def update(frame):
            ax.clear()
            
            if frame < len(steps):
                state = steps[frame]
                current_node = state['current']
                
                # Prepare node colors and labels
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node == current_node:
                        node_colors.append('red')  # Current node
                    elif node in [n[1] for n in state['open_set']]:
                        node_colors.append('lightyellow')  # In open set
                    elif node in visited_order[:frame]:
                        node_colors.append('lightgreen')  # Visited nodes
                    else:
                        node_colors.append('lightgray')  # Unvisited nodes
                    
                    # Show f-score and g-score on each node
                    g = state['g_score'].get(node, float('inf'))
                    f = state['f_score'].get(node, float('inf'))
                    node_labels[node] = f"{node}\ng={g if g != float('inf') else '∞'}\nf={f if f != float('inf') else '∞'}"
                
                # Prepare edge colors
                edge_colors = []
                edge_labels = {}
                for u, v, data in G.edges(data=True):
                    if u == current_node and v in graph[current_node]:
                        edge_colors.append('red')
                    else:
                        edge_colors.append('gray')
                    edge_labels[(u, v)] = str(data['weight'])
                
                # Draw the graph
                nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=8)
                nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2)
                nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)
                
                ax.set_title(f"Step {frame+1}/{len(steps)}: Visiting {current_node}\n"
                           f"Current f-score: {state['f_score'].get(current_node, float('inf'))}")
            else:
                # Final state - show complete path
                node_colors = []
                node_labels = {}
                for node in G.nodes():
                    if node in final_path:
                        node_colors.append('lightblue')
                    elif node in visited_order:
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')
                    
                    # Show final scores
                    g = steps[-1]['g_score'].get(node, float('inf'))
                    f = steps[-1]['f_score'].get(node, float('inf'))
                    node_labels[node] = f"{node}\ng={g if g != float('inf') else '∞'}\nf={f if f != float('inf') else '∞'}"
                
                # Draw the graph
                nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800)
                nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=8)
                
                # Draw all edges
                nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=1)
                
                # Highlight path edges
                path_edges = list(zip(final_path[:-1], final_path[1:]))
                nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, 
                                     edge_color='blue', width=3)
                
                # Draw edge labels
                edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)
                
                total_cost = sum(graph[final_path[i]][final_path[i+1]] for i in range(len(final_path)-1))
                ax.set_title(f"Path found!\n{start} to {end}: Cost = {total_cost}")
            
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