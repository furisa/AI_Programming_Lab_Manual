# inject_graphs.py

import json
import matplotlib.pyplot as plt
import numpy as np
import heapq
import time
import math
import sys
import os
from io import BytesIO
import base64


# --- CODE IMPORTS (Everything defined here to run independently) ---
def heuristic_zero(n, g): return 0.0


def heuristic_manhattan(n, g): return abs(n[0] - g[0]) + abs(n[1] - g[1])


def heuristic_euclidean(n, g): return math.hypot(n[0] - g[0], n[1] - g[1])


def heuristic_chebyshev(n, g): return max(abs(n[0] - g[0]), abs(n[1] - g[1]))


HEURISTICS = {
    'zero': heuristic_zero,
    'manhattan': heuristic_manhattan,
    'euclidean': heuristic_euclidean,
    'chebyshev': heuristic_chebyshev
}


class GridWorld:
    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()

    def is_valid(self, x, y):
        return (0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.obstacles)

    def neighbors(self, node):
        x, y = node
        return [(nx, ny) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if self.is_valid(nx := x + dx, ny := y + dy)]

    @classmethod
    def create_maze(cls, maze="default", size=10):
        if maze == "empty": return cls(size, size, [])
        if maze == "sparse": return cls(size, size, [(i, size // 2) for i in range(size // 3, 2 * size // 3)])
        if maze == "dense":
            obs = []
            for i in range(size // 4, 3 * size // 4, size // 8): obs.extend([(i, j) for j in range(size)])
            return cls(size, size, obs)
        if maze == "spiral":
            obs = []
            for i in range(2, size - 2): obs.extend([(i, 2), (i, size - 3), (2, i), (size - 3, i)])
            return cls(size, size, obs)
        return cls(size, size, [(3, i) for i in range(size)] + [(i, size // 2) for i in range(size // 2, size)])


def a_star(world, start, goal, heuristic, use_opt=True, verbose=False):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    g_score = {start: 0}
    parent = {start: None}
    expansions = 0
    closed_set = set() if use_opt else None
    while open_set:
        f, g, current = heapq.heappop(open_set)
        if use_opt and current in closed_set: continue
        if use_opt: closed_set.add(current)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, expansions, g_score[goal]
        expansions += 1
        for neighbor in world.neighbors(current):
            tg = g_score[current] + 1
            if neighbor not in g_score or tg < g_score[neighbor]:
                g_score[neighbor] = tg
                fs = tg + heuristic(neighbor, goal)
                heapq.heappush(open_set, (fs, tg, neighbor))
                parent[neighbor] = current
    return None, expansions, float('inf')


class HeuristicEvaluator:
    def __init__(self, world, start, goal):
        self.world, self.start, self.goal = world, start, goal

    def evaluate_single(self, h, opt=True):
        exp_list, time_list = [], []
        for _ in range(3):
            t0 = time.perf_counter()
            p, e, c = a_star(self.world, self.start, self.goal, h, opt)
            t1 = time.perf_counter()
            if p: exp_list.append(e); time_list.append(t1 - t0)
        return {'heuristic': h.__name__, 'expansions_mean': np.mean(exp_list), 'time_mean': np.mean(time_list) * 1000}

    def compare_all(self):
        res = []
        for k, v in HEURISTICS.items():
            r = self.evaluate_single(v)
            res.append(r)
        return res


# --- GENERATE GRAPHS ---

# Use Agg backend to generate images without popping windows
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str


# 1. Setup Data
MAZE_SIZE = 15
START = (0, 0)
GOAL = (MAZE_SIZE - 1, MAZE_SIZE - 1)
world = GridWorld.create_maze("default", MAZE_SIZE)
evaluator = HeuristicEvaluator(world, START, GOAL)
results = evaluator.compare_all()

# 2. Load Notebook
notebook_file = "Lab_8_Final_Notebook.ipynb"

if not os.path.exists(notebook_file):
    print("Error: Notebook file not found.")
else:
    with open(notebook_file, 'r') as f:
        nb = json.load(f)

    # 3. Inject Graph 1: Maze (Cell Index 4)
    try:
        print("Creating Maze Graph...")
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        for x in range(world.width):
            for y in range(world.height):
                color = 'black' if (x, y) in world.obstacles else 'white'
                rect = Rectangle((x, y), 1, 1, facecolor=color, edgecolor='lightgray')
                ax.add_patch(rect)
        if START:
            c = Circle((START[0] + 0.5, START[1] + 0.5), 0.3, fc='green', ec='black')
            ax.add_patch(c);
            ax.text(START[0] + 0.5, START[1] + 0.5, 'S', ha='center', va='center', color='white', fontweight='bold')
        if GOAL:
            c = Circle((GOAL[0] + 0.5, GOAL[1] + 0.5), 0.3, fc='red', ec='black')
            ax.add_patch(c);
            ax.text(GOAL[0] + 0.5, GOAL[1] + 0.5, 'G', ha='center', va='center', color='white', fontweight='bold')
        ax.set_xlim(0, world.width);
        ax.set_ylim(0, world.height);
        ax.set_aspect('equal')
        plt.title("Lab 8: Default Maze Layout")

        img_maze = fig_to_base64(fig)
        nb['cells'][4]['outputs'] = [{'data': {'image/png': img_maze}, 'output_type': 'display_data'}]
    except Exception as e:
        print(f"Error in Maze: {e}")

    # 4. Inject Graph 2: Bar Charts (Cell Index 8)
    try:
        print("Creating Bar Graphs...")
        labels = [r['heuristic'].replace('heuristic_', '') for r in results]
        expansions = [r['expansions_mean'] for r in results]
        times = [r['time_mean'] for r in results]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.bar(labels, expansions, color='skyblue')
        ax1.set_title('Node Expansions', fontweight='bold')
        ax1.set_ylabel('Count')
        for i, v in enumerate(expansions): ax1.text(i, v + 5, str(int(v)), ha='center')

        ax2.bar(labels, times, color='orange')
        ax2.set_title('Execution Time (ms)', fontweight='bold')
        ax2.set_ylabel('Milliseconds')
        for i, v in enumerate(times): ax2.text(i, v + 0.1, f"{v:.1f}", ha='center')

        plt.suptitle('Lab 8 Performance: Muaz Nadeem', fontsize=16)
        plt.tight_layout()

        img_bars = fig_to_base64(fig)
        nb['cells'][8]['outputs'] = [{'data': {'image/png': img_bars}, 'output_type': 'display_data'}]
    except Exception as e:
        print(f"Error in Bars: {e}")

    # 5. Save Updated Notebook
    with open(notebook_file, 'w') as f:
        json.dump(nb, f, indent=2)

    print("✅ SUCCESS! Graphs injected into Notebook.")
    print("Ab 'git add .' aur 'git push' karein.")