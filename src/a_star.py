import heapq
from .grid_world import GridWorld
def a_star(world, start, goal, heuristic, use_opt=True):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    g_score = {start: 0}
    parent = {start: None}
    closed_set = set()
    while open_set:
        f, g, current = heapq.heappop(open_set)
        if use_opt and current in closed_set: continue
        if current == goal:
            path = []; curr = current
            while curr: path.append(curr); curr = parent[curr]
            return path[::-1], len(closed_set), g
        if use_opt: closed_set.add(current)
        for n in world.neighbors(current):
            tentative_g = g_score[current] + 1
            if n not in g_score or tentative_g < g_score[n]:
                g_score[n] = tentative_g
                heapq.heappush(open_set, (tentative_g + heuristic(n, goal), tentative_g, n))
                parent[n] = current
    return None, len(closed_set), float('inf')
