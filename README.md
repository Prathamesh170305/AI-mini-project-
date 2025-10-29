🧩 Maze Solver using IDDFS

An interactive AI pathfinding mini-project that uses the Iterative Deepening Depth-First Search (IDDFS) algorithm to find a path between two points in a maze.
You can generate, edit, and solve mazes directly from a simple Streamlit web interface.

🚀 Features

🔢 Editable grid — Click to toggle between walls (1) and open paths (0)

🎲 Random maze generation (guaranteed connected structure)

⚙️ Custom start and goal points

🧠 IDDFS algorithm — gradually deepens search to efficiently find a solution

📊 Path visualization using Matplotlib

⚡ Fast and interactive UI built with Streamlit

🧠 Algorithm Used — IDDFS (Iterative Deepening DFS)

The Iterative Deepening Depth-First Search algorithm combines the benefits of:

Depth-first search (DFS): memory efficiency

Breadth-first search (BFS): completeness (guarantees finding a solution)

It works by:

Starting at a small depth limit (e.g., 0).

Running DFS up to that limit.

If the goal isn’t found, increase the limit and repeat.

Stops once the goal is found or all nodes are explored.

This makes IDDFS particularly suitable for problems like maze-solving where the depth of the goal is unknown.
