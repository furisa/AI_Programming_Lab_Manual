import math
def heuristic_zero(n, g): return 0.0
def heuristic_manhattan(n, g): return abs(n[0]-g[0]) + abs(n[1]-g[1])
def heuristic_euclidean(n, g): return math.hypot(n[0]-g[0], n[1]-g[1])
HEURISTICS = {'zero': heuristic_zero, 'manhattan': heuristic_manhattan, 'euclidean': heuristic_euclidean}
