# Maze Generator and Solver

A Python-based visualizer that dynamically generates a rectangular maze and automatically solves it in real-time. This project handles grid-based pathfinding, maze topography generation, and visual state-tracking using a native graphical user interface.

## Project Contributors & Core Modules

To simulate real-world software engineering pipelines, our team split the development cycle into specialized architecture roles:

- **Nardos (System Initialization Engineer):** Designed the foundational maze architecture by implementing the maze dimensions, wall matrices (`northwall` and `eastwall`), visited-state arrays, randomized entrance and exit generation, and initial solver/generator state configuration.
- **Hilina (Solver State Engineer):** Developed the solver initialization and reset system, including automated state preparation, stack initialization, and synchronization between the maze generator and solving phases.
- **Mekdelawit (Maze Generation Architect):** Engineered the randomized Depth-First Search (DFS) maze generation algorithm, including neighbor detection, stack-based traversal, recursive-style backtracking, wall-carving mechanics, and rogue-wall challenge extensions.
- **Hanan (Pathfinding & Traversal Engineer):** Implemented the maze-solving engine using logical traversal and backtracking techniques, including valid-path detection, dead-end isolation, path memory tracking, and solver navigation control.
- **Dagim (Graphics & Visualization Engineer):** Built the Tkinter rendering pipeline, including maze wall visualization, solver path rendering, dead-end highlighting, animation updates, active-state tracking visualization, and the continuous GUI event loop system.

## 1. Rendering Engine & Data Visualization

The application uses Python's built-in `tkinter` library to handle 2D graphics natively without requiring heavy external 3D drivers. This ensures smooth performance and cross-platform compatibility out of the box.

### Maze Logic Arrays

The structural architecture relies on two 2D matrices that keep track of which walls are currently standing:

- `northwall`: Stores the presence of horizontal walls (cell ceilings).
- `eastwall`: Stores the presence of vertical walls (cell right-side boundaries).
- **Initialization:** Both matrices are filled with `1` (solid True), meaning the maze begins as a completely sealed grid. To carve pathways, the generation algorithm selectively flips these values to `0`.

### Rendering Pipeline

The `draw_maze()` function constantly updates the canvas by converting these mathematical matrices into clean visual geometry:

- **Coordinate Remapping:** Translates 1-based grid coordinates into pixel locations on the screen. Because standard UI layouts treat the top-left as `(0,0)`, the engine flips the Y-axis calculation (`HEIGHT - (i * CELL_SIZE)`) so that the visual orientation aligns perfectly with the logical rows.
- **Perimeter Preservation:** The drawing loops are specifically calibrated to render the phantom row `0` and column `0`. This securely closes the outer top and bottom perimeters while leaving clear open gaps where the entrance and exit are located.

## 2. Maze Generation (The "Eater" Mouse)

The goal of the generator is to transform a solid block of cells into a perfectly interconnected, navigable puzzle.

- **The DFS Algorithm:** The program executes a randomized Depth-First Search (DFS) backed by a custom stack list.
- **The Carving Mechanism:** An invisible "mouse" spawns at a randomly assigned starting row on the left edge (column 1) and actively scans its four immediate cardinal directions for unvisited cells.
  - It selects a valid neighbor at random, pushes the current cell to the stack, and moves forward. As it crosses the boundary, it sets the corresponding value in `northwall` or `eastwall` to `0`—effectively "eating" through the wall.
  - When the mouse hits a dead end (surrounded entirely by visited cells), it utilizes the stack to backtrack to the most recent cell with open options and continues carving.
- **Rogue Logic (Cycle Generation):** Standard DFS mazes form a strict "spanning tree" with only one true path between any two points. To make things more complex, a 1-in-20 chance was injected into the loop. When triggered, the mouse eats a random adjacent wall regardless of whether that neighbor was visited. This builds loops and cycles in the grid, purposefully breaking simple "shoulder-to-the-wall" routing rules.

## 3. Solver and Pathfinding Logic

Once the stack clears and the maze generation concludes, control is automatically handed over to a second pathfinding routine.

- **Movement Restrictions:** Unlike the generator, the solver mouse is completely bound by physical logic; it can only step into an adjacent cell if the shared wall matrix value is `0`.
- **Search Strategy:** It uses its own stack-based DFS to hunt for the exit gap on the rightmost edge.
- **Loop Prevention:** Because the generator introduced rogue cycles, a simple wall-follower could get trapped spinning in circles forever. To counter this, the solver manages an isolated `solve_visited` matrix, ensuring it never enters an infinite loop.
- **Visual State Management:**
  - **The Active Path (Green Dots):** The true, live path currently stored in `solve_stack` is rendered as bright green circles.
  - **The Dead Ends (Blue Dots):** When the solver hits a dead end, it pops the cell off its stack and permanently saves its coordinates into a `dead_ends` list. These cells turn into distinct blue dots on the screen. This tells the viewer exactly which paths were explored and abandoned.
  - **The Active Mouse (Red Square):** A standalone red square tracks the exact head of the search operation at all times.

## Design & Architecture Questions

### Might a queue be better than a stack for storing candidates during generation? How would it affect the paths?

No, switching from a stack to a queue would fundamentally transform the algorithm from a Depth-First Search (DFS) to a **Breadth-First Search (BFS)**. Instead of carving out long, winding, organic corridors, a queue would force the path generation to expand uniformly outward in all directions from the starting point at the exact same time. This results in a highly geometric, short, circular maze layout that lacks the classic complexity of long-form maze pathways.

### Why can starting and ending cells be on outer boundaries with cycles, and you will still always find the end using the "shoulder-to-the-wall" method?

If both the entrance and exit are placed on the absolute outer boundaries of the maze, the perimeter wall itself acts as one unbroken, continuous topological line connecting the start to the finish. Even if the rogue logic creates isolated loop "islands" inside the interior of the grid, keeping your hand pinned strictly to the outer boundary ensures you navigate cleanly around those loops without getting caught in an endless circuit.

## How to Run the Project

### Requirements

- **Python 3.x** (Tested and fully compatible up to Python 3.14+).
- **Zero External Dependencies:** Because this version uses Python's standard `tkinter` library, you do not need to install `pygame`, `PyOpenGL`, or run any `pip install` commands.

### Execution Steps

1. Navigate to the directory where `maze.py` is saved.
2. Run the script via terminal:
   ```bash
   python maze.py
   ```
