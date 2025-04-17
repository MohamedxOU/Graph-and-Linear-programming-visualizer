# Algorithm Visualizer

Algorithm Visualizer is a PyQt6-based desktop application designed to help users understand and visualize various algorithms, including graph algorithms (BFS, DFS, and Greedy Coloring) and linear programming algorithms (Simplex). The application provides an intuitive user interface for inputting data and visualizing the results.

## Features

- **Graph Algorithms**:
  - **Breadth-First Search (BFS)**: Visualize the traversal of a graph using BFS.
  - **Depth-First Search (DFS)**: Visualize the traversal of a graph using DFS.
  - **Greedy Graph Coloring**: Visualize the coloring of a graph using a greedy algorithm.

- **Linear Programming Algorithms** (Planned):
  - Simplex algorithm for solving linear programming problems.

- **Interactive Input**:
  - Input graphs as adjacency lists or dictionaries.
  - Add or modify graph nodes and edges dynamically.

- **Visualization**:
  - Graph traversal and coloring visualized using `matplotlib` and `networkx`.

- **Modern UI**:
  - Styled with a custom CSS theme for a clean and modern look.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MohamedxOU/Graph-and-Linear-programming-visualizer.git
   cd Graph-and-Linear-programming-visualizer

   pip install -r requirements.txt

   python main.py

## Usage

1. **Launch the Application**:
    Run the following command to start the application:
    ```bash
    python main.py
    ```

2. **Select an Algorithm**:
    - Choose the desired algorithm (BFS, DFS, Greedy Coloring, or Simplex) from the main menu.

3. **Input Data**:
    - For graph algorithms:
      - Input the graph as an adjacency list or dictionary.
      - Add or modify nodes and edges dynamically using the interface.
    - For linear programming (Simplex):
      - Input the objective function and constraints (feature under development).

4. **Visualize**:
    - Click the "Visualize" button to see the algorithm in action.
    - The graph traversal or coloring will be displayed using `matplotlib` and `networkx`.

5. **Export Results** (Optional):
    - Save the visualization or results to a file for later reference.

6. **Exit**:
    - Close the application when done.

For detailed examples and tutorials, refer to the documentation or visit the project's GitHub repository.



