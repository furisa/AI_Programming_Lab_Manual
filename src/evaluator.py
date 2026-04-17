import time
from src.grid_world import GridWorld
from src.a_star import a_star
from src.heuristics import HEURISTICS
def compare_heuristics():
    world = GridWorld.create_maze("spiral", 15)
    start, goal = (0,0), (14,14)
    print(f"Running A* on Spiral Maze...")
    for name, h in HEURISTICS.items():
        t = time.perf_counter()
        path, exp, cost = a_star(world, start, goal, h)
        elapsed = (time.perf_counter() - t) * 1000
        print(f"  {name:12} | Path: {'Found' if path else 'No'} | Expansions: {exp:4} | Time: {elapsed:6.2f}ms")
