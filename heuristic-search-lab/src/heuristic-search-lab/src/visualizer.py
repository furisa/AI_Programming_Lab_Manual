
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
from typing import List, Tuple, Optional
from .grid_world import GridWorld

class PathVisualizer:
    @staticmethod
    def visualize_world(world, path=None, start=None, goal=None, title="Grid World"):
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        for x in range(world.width):
            for y in range(world.height):
                color = 'black' if (x,y) in world.obstacles else 'white'
                rect = Rectangle((x, y), 1, 1, facecolor=color, edgecolor='lightgray')
                ax.add_patch(rect)
        if path:
            px, py = [p[0]+0.5 for p in path], [p[1]+0.5 for p in path]
            ax.plot(px, py, 'b-', lw=3, label='Path')
            ax.scatter(px, py, c='blue', s=40)
        if start:
            c = Circle((start[0]+0.5, start[1]+0.5), 0.3, fc='green', ec='black')
            ax.add_patch(c); ax.text(start[0]+0.5, start[1]+0.5, 'S', ha='center', va='center', color='white', fontweight='bold')
        if goal:
            c = Circle((goal[0]+0.5, goal[1]+0.5), 0.3, fc='red', ec='black')
            ax.add_patch(c); ax.text(goal[0]+0.5, goal[1]+0.5, 'G', ha='center', va='center', color='white', fontweight='bold')
        ax.set_xlim(0, world.width); ax.set_ylim(0, world.height); ax.set_aspect('equal')
        plt.title(title); plt.show()
