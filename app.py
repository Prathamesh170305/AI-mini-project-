import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ------------------------------
# Maze Generator (connected)
# ------------------------------
def generate_connected_maze(rows, cols, wall_prob=0.3):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    start = (0, 0)
    stack = [start]
    visited = set([start])

    while stack:
        r, c = stack.pop()
        maze[r][c] = 0
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if random.random() > wall_prob:
                    maze[nr][nc] = 0
                visited.add((nr, nc))
                stack.append((nr, nc))
    return maze

# ------------------------------
# IDDFS Algorithm
# ------------------------------
def iddfs(maze, start, goal, max_depth):
    for depth in range(max_depth + 1):
        visited = set()
        path = []
        found = dls(maze, start, goal, depth, visited, path)
        if found:
            return path[::-1], depth
    return None, max_depth

def dls(maze, node, goal, depth, visited, path):
    if depth < 0:
        return False
    r, c = node
    if node == goal:
        path.append(node)
        return True
    visited.add(node)
    rows, cols = len(maze), len(maze[0])
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if (0 <= nr < rows and 0 <= nc < cols and
            maze[nr][nc] == 0 and (nr, nc) not in visited):
            if dls(maze, (nr, nc), goal, depth - 1, visited, path):
                path.append(node)
                return True
    return False

# ------------------------------
# Visualization
# ------------------------------
def visualize_maze(maze, path, start, goal):
    maze_display = np.array(maze, dtype=float)
    for (r, c) in path:
        maze_display[r, c] = 0.5
    maze_display[start[0], start[1]] = 0.3
    maze_display[goal[0], goal[1]] = 0.8

    fig, ax = plt.subplots()
    cmap = plt.cm.get_cmap("coolwarm", 4)
    ax.imshow(maze_display, cmap=cmap)
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Maze Solver using IDDFS", page_icon="🧩", layout="centered")
st.title("🧩 Maze Solver using IDDFS (Editable Grid)")

st.markdown("Create or edit your own maze, set start and goal, and let **IDDFS** find the path!")

# Grid size
rows = st.slider("Select maze rows", 5, 15, 8)
cols = st.slider("Select maze columns", 5, 15, 8)
random_maze = st.checkbox("Generate Random Solvable Maze", value=True)

# Maze generation
if random_maze:
    maze = generate_connected_maze(rows, cols)
else:
    maze = [[0 for _ in range(cols)] for _ in range(rows)]

# Start and Goal input
st.write("### Define Start & Goal positions")
col1, col2 = st.columns(2)
with col1:
    start_r = st.number_input("Start Row", 0, rows-1, 0)
    start_c = st.number_input("Start Col", 0, cols-1, 0)
with col2:
    goal_r = st.number_input("Goal Row", 0, rows-1, rows-1)
    goal_c = st.number_input("Goal Col", 0, cols-1, cols-1)

start = (start_r, start_c)
goal = (goal_r, goal_c)

# Keep start and goal open
maze[start_r][start_c] = 0
maze[goal_r][goal_c] = 0

st.markdown("### 🧱 Edit Maze (0 = Path, 1 = Wall)")
editable_maze = st.data_editor(
    pd.DataFrame(maze),
    use_container_width=True,
    num_rows="dynamic",
    key="maze_editor"
)

# Convert DataFrame back to list of lists
maze = editable_maze.values.tolist()

# Protect start & goal
maze[start_r][start_c] = 0
maze[goal_r][goal_c] = 0

# Display for clarity
st.write("Maze grid ready for solving:")

# Solve button
if st.button("🔍 Solve Maze"):
    with st.spinner("Running IDDFS..."):
        start_time = time.time()
        max_depth = rows * cols
        path, used_depth = iddfs(maze, start, goal, max_depth)
        end_time = time.time()

        if path:
            st.success(f"✅ Path found! Length: {len(path)} | Depth used: {used_depth} | Time: {end_time - start_time:.3f}s")
            visualize_maze(maze, path, start, goal)
        else:
            st.error("❌ No path found in this maze configuration.")

