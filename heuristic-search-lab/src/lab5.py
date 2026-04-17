import json, base64, io, sys, os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, '..')
from src.utils import set_seed
from src.state import RobotState
from src.problem import WarehouseProblem
from src.search import UniformCostSearch

os.makedirs('../notebooks', exist_ok=True)
os.makedirs('../outputs', exist_ok=True)


def md(text): return {"cell_type": "markdown", "id": "m" + str(hash(text))[:8], "metadata": {},
                      "source": text.split('\n')}


def code(c, out="", img=None):
    o = []
    if out.strip(): o.append({"output_type": "stream", "name": "stdout", "text": out.split('\n')})
    if img and os.path.exists(img):
        with open(img, "rb") as f: b = base64.b64encode(f.read()).decode('utf-8')
        o.append({"output_type": "display_data", "data": {"image/png": b}, "metadata": {}})
    return {"cell_type": "code", "id": "c" + str(hash(c))[:8], "metadata": {}, "source": c.split('\n'), "outputs": o,
            "execution_count": None}


def run(c):
    old = sys.stdout;
    sys.stdout = b = io.StringIO()
    try:
        exec(c, globals()); out = b.getvalue()
    except Exception as e:
        out = f"Error: {e}\n"
    finally:
        sys.stdout = old
    return out


def solve_and_plot(grid, title):
    set_seed(42)
    pkgs, deli, start = [], None, None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'P':
                pkgs.append((i, j))
            elif grid[i][j] == 'D':
                deli = (i, j)
            elif grid[i][j] == 'S':
                start = (i, j)

    prob = WarehouseProblem(grid, pkgs, deli)
    init = RobotState(start, frozenset())
    ucs = UniformCostSearch(prob)
    path, cost, nodes, t = ucs.solve(init)

    plt.figure(figsize=(6, 6))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'X':
                plt.scatter(j, -i, color='black', s=200, marker='s')
            elif grid[i][j] == 'S':
                plt.scatter(j, -i, color='blue', s=200, marker='o', label='Start')
            elif grid[i][j] == 'D':
                plt.scatter(j, -i, color='red', s=200, marker='*', label='Delivery')
            elif grid[i][j] == 'P':
                plt.scatter(j, -i, color='green', s=200, marker='^', label='Package')
    if path:
        px, py = zip(*path)
        plt.plot(px, [-y for y in py], color='orange', linewidth=3, label=f'Path (Cost: {cost})')
    plt.legend();
    plt.title(title);
    plt.grid(True)
    p = f"../outputs/{title.replace(' ', '_')}.png"
    plt.savefig(p, dpi=150);
    plt.close()
    return path, cost, nodes, t, p


cells = []
cells.append(md("""# Lab 5: Warehouse Robot AI - Complete Tutorial
**Name:** Muhammad Muaz  
**Program:** BS Artificial Intelligence  
**Objective:** AI Search (UCS), State Space, Version Control Integration"""))

cells.append(md("""## Phase 1 & 2: Project Setup & State Space Design
- Implemented `RobotState` and `WarehouseProblem` classes.
- Designed Uniform Cost Search (UCS) to find minimum cost path.
- Rules: Cost=1/move, Cannot pass 'X', Must collect all 'P' before 'D'."""))

c = """import sys, os
sys.path.insert(0, '..')
from src.utils import set_seed
from src.state import RobotState
from src.problem import WarehouseProblem
from src.search import UniformCostSearch
print("Classes imported successfully!")"""
cells.append(code(c, run(c)))

cells.append(md("""## Phase 5: Experiment 1 - Simple 5x5 Grid"""))

c = """grid1 = [
    ['S', '.', '.', 'X', '.'],
    ['.', 'P', '.', 'X', '.'],
    ['.', '.', '.', '.', '.'],
    ['X', '.', 'P', '.', '.'],
    ['.', '.', '.', 'D', '.']
]
path1, cost1, nodes1, time1, _ = solve_and_plot(grid1, "Simple 5x5 Grid")
print(f"Status: {'Found' if path1 else 'Not Found'}")
print(f"Cost: {cost1}, Nodes Expanded: {nodes1}, Time: {time1:.4f}s")
print(f"Path: {path1}")"""
cells.append(code(c, run(c), "../outputs/Simple_5x5_Grid.png"))

cells.append(md("""## Phase 5: Experiment 2 - Medium 8x8 Grid"""))

c = """grid2 = [
    ['S', '.', '.', 'X', '.', '.', '.', '.'],
    ['.', 'P', '.', 'X', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'X', '.', '.', '.'],
    ['X', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'X', '.'],
    ['.', '.', '.', '.', '.', '.', 'D', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
]
path2, cost2, nodes2, time2, _ = solve_and_plot(grid2, "Medium 8x8 Grid")
print(f"Status: {'Found' if path2 else 'Not Found'}")
print(f"Cost: {cost2}, Nodes Expanded: {nodes2}, Time: {time2:.4f}s")"""
cells.append(code(c, run(c), "../outputs/Medium_8x8_Grid.png"))

cells.append(md("""## Phase 6: Testing & Validation (Simulated pytest)
*Note: `pytest` bypassed due to environment constraints, tested natively.*"""))

c = """# Running Unit Tests natively
from src.state import RobotState
from src.problem import WarehouseProblem

# Test 1: State Equality
s1 = RobotState((0, 0), frozenset([(1, 1)]))
s2 = RobotState((0, 0), frozenset([(1, 1)]))
print("Test Equality:", "PASSED" if s1 == s2 else "FAILED")

# Test 2: Hashing
print("Test Hash:", "PASSED" if hash(s1) == hash(s2) else "FAILED")

# Test 3: Neighbors
grid = [['S', '.'], ['.', 'D']]
prob = WarehouseProblem(grid, [], (1, 1))
state = RobotState((0, 0))
print("Test Neighbors:", "PASSED" if len(state.get_neighbors(prob)) == 2 else "FAILED")

# Test 4: Package Collection
grid2 = [['S', 'P'], ['.', 'D']]
prob2 = WarehouseProblem(grid2, [(0, 1)], (1, 1))
state2 = RobotState((0, 0))
nbrs = state2.get_neighbors(prob2)
pkg_collected = any((0, 1) in n.collected for n in nbrs if n.position == (0, 1))
print("Test Package:", "PASSED" if pkg_collected else "FAILED")"""
cells.append(code(c, run(c)))

cells.append(md("""## Conclusion
Successfully formulated the Warehouse Robot problem as a State Space Search.
- **UCS** guarantees the shortest path.
- **State** tracks both robot position AND collected packages using `frozenset`.
- **Reproducibility** ensured via `set_seed(42)`.
- Complex grids (8x8) take slightly more nodes to expand but accurately avoid obstacles."""))

nb = {"nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "cells": cells}
with open('../notebooks/lab5_warehouse_robot.ipynb', 'w') as f: json.dump(nb, f, indent=1)
print("\n" + "=" * 50)
print("✅ SUCCESS! Lab 5 NOTEBOOK GENERATED!")
print("=" * 50)