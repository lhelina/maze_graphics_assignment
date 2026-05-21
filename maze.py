import tkinter as tk
import random

# Dimensions requested by assignment (R rows by C columns)
R, C = 20, 25
CELL_SIZE = 30
WIDTH = C * CELL_SIZE
HEIGHT = R * CELL_SIZE

# --- ASSIGNMENT DATA STRUCTURES ---
# 1-based index mapping: cells range from row 1..R and col 1..C.
# northwall[i][j] == 1 means cell (i,j) has a solid upper (north) wall.
# eastwall[i][j] == 1 means cell (i,j) has a solid right (east) wall.
# Row 0 acts as a phantom row whose north walls form the bottom edge of the maze.
# Column 0 acts as a phantom column whose east walls form the left edge of the maze.
northwall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
eastwall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]

# Random entrance (left edge, col 1) and exit (right edge, col C)
start_i = random.randint(1, R)
start_j = 1
end_i = random.randint(1, R)
end_j = C

# Open the outer edge walls for entrance and exit
eastwall[start_i][0] = 0   # Left edge opening
eastwall[end_i][C] = 0     # Right edge opening

# Set up the generation mouse
curr_i, curr_j = start_i, start_j
visited[curr_i][curr_j] = True

stack = []
generating = True

# Set up the solver tracking
solving = False
solve_stack = []
dead_ends = []
solve_visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]

solve_i, solve_j = start_i, start_j
solve_visited[solve_i][solve_j] = True

def setup_solver():
    global solving, solve_i, solve_j
    solving = True
    # Clean reset of solver parameters to match random assignment start
    solve_i, solve_j = start_i, start_j
    solve_stack.clear()
    solve_stack.append((solve_i, solve_j))
    solve_visited[solve_i][solve_j] = True

