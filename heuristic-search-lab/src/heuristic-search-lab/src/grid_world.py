
import numpy as np
from typing import List, Tuple, Set, Optional

class GridWorld:
    def __init__(self, width: int, height: int, obstacles: Optional[List[Tuple[int, int]]] = None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()

    def is_valid(self, x: int, y: int) -> bool:
        return (0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.obstacles)

    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = node
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [(nx, ny) for dx, dy in directions if self.is_valid(nx := x + dx, ny := y + dy)]

    @classmethod
    def create_maze(cls, maze_type: str = "default", size: int = 10):
        if maze_type == "empty": return cls(size, size, [])
        if maze_type == "sparse": return cls(size, size, [(i, size//2) for i in range(size//3, 2*size//3)])
        if maze_type == "dense":
            obs = []
            for i in range(size//4, 3*size//4, size//8): obs.extend([(i, j) for j in range(size)])
            return cls(size, size, obs)
        if maze_type == "spiral":
            obs = []
            for i in range(2, size-2): obs.extend([(i, 2), (i, size-3), (2, i), (size-3, i)])
            return cls(size, size, obs)
        # Default
        return cls(size, size, [(3, i) for i in range(size)] + [(i, size//2) for i in range(size//2, size)])
