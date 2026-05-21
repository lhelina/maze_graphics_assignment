import tkinter as tk
import random

# Dimensions (R rows by C columns)
R, C = 20, 25
CELL_SIZE = 30
WIDTH = C * CELL_SIZE
HEIGHT = R * CELL_SIZE

# data structures
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


def generate_step():
    global curr_i, curr_j, generating

    neighbours = []

    # Look for unvisited neighbors (1-based boundaries)
    if curr_i < R and not visited[curr_i + 1][curr_j]:
        neighbours.append(('N', curr_i + 1, curr_j))
    if curr_i > 1 and not visited[curr_i - 1][curr_j]:
        neighbours.append(('S', curr_i - 1, curr_j))
    if curr_j < C and not visited[curr_i][curr_j + 1]:
        neighbours.append(('E', curr_i, curr_j + 1))
    if curr_j > 1 and not visited[curr_i][curr_j - 1]:
        neighbours.append(('W', curr_i, curr_j - 1))

    if neighbours:
        direction, next_i, next_j = random.choice(neighbours)
        stack.append((curr_i, curr_j))

        # --- CORRECTED WALL BREAKING LOGIC ---
        # northwall[i][j] is the ceiling of (i,j). eastwall[i][j] is the right wall of (i,j).
        if direction == 'N': 
            northwall[curr_i][curr_j] = 0
        elif direction == 'S': 
            northwall[curr_i - 1][curr_j] = 0
        elif direction == 'E': 
            eastwall[curr_i][curr_j] = 0
        elif direction == 'W': 
            eastwall[curr_i][curr_j - 1] = 0

        # --- CHALLENGE BONUS: 1 in 20 chance to eat an extra wall ---
        if random.randint(1, 20) == 1:
            extra_dirs = []
            if curr_i < R: extra_dirs.append('N')
            if curr_i > 1: extra_dirs.append('S')
            if curr_j < C: extra_dirs.append('E')
            if curr_j > 1: extra_dirs.append('W')

            if extra_dirs:
                rogue_dir = random.choice(extra_dirs)
                if rogue_dir == 'N': northwall[curr_i][curr_j] = 0
                elif rogue_dir == 'S': northwall[curr_i - 1][curr_j] = 0
                elif rogue_dir == 'E': eastwall[curr_i][curr_j] = 0
                elif rogue_dir == 'W': eastwall[curr_i][curr_j - 1] = 0

        curr_i, curr_j = next_i, next_j
        visited[curr_i][curr_j] = True

    elif stack:
        curr_i, curr_j = stack.pop()
    else:
        generating = False
        setup_solver()
def solve_step():
    global solve_i, solve_j, solving

    if solve_i == end_i and solve_j == end_j:
        solving = False
        return

    neighbours = []

    # Check for paths with NO walls that haven't been visited by the solver yet
    if solve_i < R and northwall[solve_i][solve_j] == 0 and not solve_visited[solve_i + 1][solve_j]:
        neighbours.append((solve_i + 1, solve_j))
    if solve_i > 1 and northwall[solve_i - 1][solve_j] == 0 and not solve_visited[solve_i - 1][solve_j]:
        neighbours.append((solve_i - 1, solve_j))
    if solve_j < C and eastwall[solve_i][solve_j] == 0 and not solve_visited[solve_i][solve_j + 1]:
        neighbours.append((solve_i, solve_j + 1))
    if solve_j > 1 and eastwall[solve_i][solve_j - 1] == 0 and not solve_visited[solve_i][solve_j - 1]:
        neighbours.append((solve_i, solve_j - 1))

    if neighbours:
        solve_stack.append((solve_i, solve_j))
        solve_i, solve_j = random.choice(neighbours)
        solve_visited[solve_i][solve_j] = True
    elif solve_stack:
        # Mark dead end as blue trail and backtrack
        dead_ends.append((solve_i, solve_j))
        solve_i, solve_j = solve_stack.pop()
    else:
        solving = False

