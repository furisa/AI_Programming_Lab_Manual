import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.grid_world import GridWorld
from src.evaluator import compare_heuristics

def create_maze(type, size):
    if type == "spiral":
        obs = []
        for i in range(2, size-2): obs.extend([(i,2), (i,size-3), (2,i), (size-3,i)])
        return GridWorld(size, size, obs)
    return GridWorld(size, size)

GridWorld.create_maze = create_maze
if __name__ == "__main__":
    compare_heuristics()
