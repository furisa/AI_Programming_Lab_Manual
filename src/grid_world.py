import numpy as np
from typing import List, Tuple
class GridWorld:
    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()
    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and (x,y) not in self.obstacles
    def neighbors(self, node):
        x,y = node
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        return [(x+dx, y+dy) for dx,dy in dirs if self.is_valid(x+dx, y+dy)]
    def visualize(self, path=None, start=None, goal=None):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6,6))
        for x in range(self.width):
            for y in range(self.height):
                c = 'black' if (x,y) in self.obstacles else 'white'
                rect = plt.Rectangle((x,y), 1, 1, facecolor=c, edgecolor='gray')
                ax.add_patch(rect)
        if path:
            px, py = zip(*path)
            ax.plot([p+0.5 for p in px], [p+0.5 for p in py], 'b-', linewidth=2)
        if start: ax.add_patch(plt.Circle((start[0]+0.5, start[1]+0.5), 0.3, color='green'))
        if goal: ax.add_patch(plt.Circle((goal[0]+0.5, goal[1]+0.5), 0.3, color='red'))
        ax.set_xlim(0, self.width); ax.set_ylim(0, self.height)
        plt.grid(True, alpha=0.3); plt.show()
