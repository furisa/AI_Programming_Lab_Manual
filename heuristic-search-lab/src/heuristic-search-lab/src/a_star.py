
import heapq
from typing import Dict, List, Tuple, Optional, Callable
from .grid_world import GridWorld

def a_star(world: GridWorld, start: Tuple[int, int], goal: Tuple[int, int], 
           heuristic: Callable, use_optimization: bool = True, verbose: bool = False):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    g_score = {start: 0}
    parent = {start: None}
    expansions = 0
    closed_set = set() if use_optimization else None

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if use_optimization and current in closed_set: continue
        if use_optimization: closed_set.add(current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, expansions, g_score[goal]

        expansions += 1
        for neighbor in world.neighbors(current):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                parent[neighbor] = current
    return None, expansions, float('inf')
