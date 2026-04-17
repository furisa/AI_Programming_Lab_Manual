
import time
import numpy as np
from typing import Dict, List, Tuple, Callable
from .grid_world import GridWorld
from .a_star import a_star
from .heuristics import HEURISTICS

class HeuristicEvaluator:
    def __init__(self, world, start, goal):
        self.world, self.start, self.goal = world, start, goal

    def evaluate_single(self, heuristic, use_optimization=True, num_trials=3):
        expansions_list, time_list = [], []
        for _ in range(num_trials):
            t0 = time.perf_counter()
            path, exp, cost = a_star(self.world, self.start, self.goal, heuristic, use_optimization)
            t1 = time.perf_counter()
            if path:
                expansions_list.append(exp)
                time_list.append(t1-t0)
        return {
            'heuristic': heuristic.__name__, 'optimization': use_optimization,
            'expansions_mean': np.mean(expansions_list) if expansions_list else 0,
            'time_mean': np.mean(time_list)*1000 if time_list else 0
        }

    def compare_all(self, heuristic_names=None):
        if heuristic_names is None: heuristic_names = list(HEURISTICS.keys())
        results = []
        for name in heuristic_names:
            res = self.evaluate_single(HEURISTICS[name])
            results.append(res)
            print(f"{name:12} | Exp: {res['expansions_mean']:.0f} | Time: {res['time_mean']:.2f}ms")
        return results
