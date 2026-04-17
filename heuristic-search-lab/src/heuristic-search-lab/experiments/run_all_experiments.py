# run_all_tests.py

import sys
import os

# Src folder ko path mein add kar rahe hain
sys.path.append(os.getcwd())

import time
from src.grid_world import GridWorld
from src.a_star import a_star
from src.heuristics import (
    heuristic_manhattan,
    heuristic_euclidean,
    heuristic_chebyshev,
    heuristic_zero
)


def test_astar_path_finding():
    """Test 1: Check if A* finds a valid path from (0,0) to (5,5)"""
    print("🧪 Running Test 1: A* Path Finding...")

    # Chota sa grid bana rahe hain test ke liye
    world = GridWorld(10, 10, obstacles=[(2, 2), (2, 3)])
    start = (0, 0)
    goal = (5, 5)

    path, expansions, cost = a_star(world, start, goal, heuristic_manhattan)

    if path is None:
        print("   ❌ FAILED: Path not found")
        return False

    if path[0] != start or path[-1] != goal:
        print(f"   ❌ FAILED: Path does not start or end correctly. Start: {path[0]}, Goal: {path[-1]}")
        return False

    # Check if consecutive nodes are neighbors (valid step)
    for i in range(len(path) - 1):
        curr, next_node = path[i], path[i + 1]
        # Manhattan distance between consecutive nodes should be 1
        dist = abs(curr[0] - next_node[0]) + abs(curr[1] - next_node[1])
        if dist != 1:
            print(f"   ❌ FAILED: Invalid step between {curr} and {next_node}")
            return False

    print(f"   ✅ PASSED: Valid path found (Length: {len(path)}, Cost: {cost})")
    return True


def test_heuristic_logic():
    """Test 2: Check if Heuristics give correct values"""
    print("🧪 Running Test 2: Heuristic Logic Check...")

    node = (0, 0)
    goal = (3, 4)

    # Manhattan: |0-3| + |0-4| = 3 + 4 = 7
    h_man = heuristic_manhattan(node, goal)
    if h_man != 7:
        print(f"   ❌ FAILED: Manhattan distance should be 7, got {h_man}")
        return False

    # Euclidean: sqrt(3^2 + 4^2) = 5.0
    h_euc = heuristic_euclidean(node, goal)
    if h_euc != 5.0:
        print(f"   ❌ FAILED: Euclidean distance should be 5.0, got {h_euc}")
        return False

    # Chebyshev: max(|0-3|, |0-4|) = 4
    h_cheb = heuristic_chebyshev(node, goal)
    if h_cheb != 4:
        print(f"   ❌ FAILED: Chebyshev distance should be 4, got {h_cheb}")
        return False

    print(f"   ✅ PASSED: All heuristics calculated correctly")
    return True


def test_admissibility():
    """Test 3: Check if heuristics are admissible (never overestimate)"""
    print("🧪 Running Test 3: Admissibility Check...")

    world = GridWorld(5, 5, [])
    start = (0, 0)
    goal = (4, 4)

    # Find Optimal Cost using Dijkstra (Zero Heuristic)
    _, _, optimal_cost = a_star(world, start, goal, heuristic_zero, use_optimization=False)

    # Find Cost using Manhattan
    _, _, manhattan_cost = a_star(world, start, goal, heuristic_manhattan, use_optimization=False)

    # A* with admissible heuristic should find optimal cost (same as Dijkstra)
    if manhattan_cost != optimal_cost:
        print(f"   ❌ FAILED: Heuristic overestimated. Optimal: {optimal_cost}, Found: {manhattan_cost}")
        return False

    print(f"   ✅ PASSED: Heuristic is admissible (Optimal: {optimal_cost})")
    return True


# --- Main Execution ---
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(" LAB 8: AUTOMATED TEST SUITE ")
    print("=" * 50 + "\n")

    results = []

    # Run all tests
    results.append(("A* Path Finding", test_astar_path_finding()))
    results.append(("Heuristic Logic", test_heuristic_logic()))
    results.append(("Admissibility Check", test_admissibility()))

    # Summary
    print("\n" + "=" * 50)
    print(" SUMMARY REPORT ")
    print("=" * 50)

    passed_count = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} : {status}")
        if result: passed_count += 1

    print(f"\nTotal: {passed_count}/{len(results)} Tests Passed")
    print("=" * 50)