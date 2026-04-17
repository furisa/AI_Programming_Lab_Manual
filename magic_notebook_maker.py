import os
import json

# Ensure folder exists
os.makedirs("notebooks", exist_ok=True)

# Define the Notebook Content (JSON format)
notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🚀 Heuristic Search: Auto-Generated Report\n",
                "\n",
                "Ye notebook automatically generate hui hai. Niche graphs aur code diye gaye hain."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Setup and Imports\n",
                "import sys\n",
                "import os\n",
                "sys.path.append(os.path.abspath('..')) # Go to parent folder\n",
                "\n",
                "from src.grid_world import GridWorld\n",
                "from src.a_star import a_star\n",
                "from src.heuristics import HEURISTICS\n",
                "\n",
                "import matplotlib.pyplot as plt\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "\n",
                "print(\"Libraries Imported Successfully!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Create a Spiral Maze"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Factory method for Spiral Maze\n",
                "def create_maze(type, size):\n",
                "    if type == \"spiral\":\n",
                "        obs = []\n",
                "        for i in range(2, size-2): \n",
                "            obs.extend([(i,2), (i,size-3), (2,i), (size-3,i)])\n",
                "        return GridWorld(size, size, obs)\n",
                "    return GridWorld(size, size)\n",
                "\n",
                "world = create_maze(\"spiral\", 15)\n",
                "start, goal = (0, 0), (14, 14)\n",
                "\n",
                "# Visualize Empty Maze\n",
                "world.visualize(start=start, goal=goal, title=\"Spiral Maze (15x15)\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Run A* & Compare Heuristics"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import time\n",
                "\n",
                "results = []\n",
                "\n",
                "print(f\"{'Heuristic':<15} | {'Time (ms)':<10} | {'Expansions':<10}\")\n",
                "print(\"-\" * 45)\n",
                "\n",
                "for name, heuristic_func in HEURISTICS.items():\n",
                "    t_start = time.perf_counter()\n",
                "    path, expansions, cost = a_star(world, start, goal, heuristic_func)\n",
                "    t_end = time.perf_counter()\n",
                "    \n",
                "    time_ms = (t_end - t_start) * 1000\n",
                "    \n",
                "    results.append({\n",
                "        'Name': name,\n",
                "        'Time': time_ms,\n",
                "        'Expansions': expansions,\n",
                "        'Path': path\n",
                "    })\n",
                "    \n",
                "    print(f\"{name:<15} | {time_ms:<10.2f} | {expansions:<10}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Performance Graphs 📊"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create a DataFrame for clean plotting\n",
                "df = pd.DataFrame(results)\n",
                "\n",
                "# Plot 1: Time Comparison\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                "\n",
                "ax1.bar(df['Name'], df['Time'], color=['skyblue', 'orange', 'green'])\n",
                "ax1.set_title('Algorithm Speed (Time)')\n",
                "ax1.set_ylabel('Time (ms)')\n",
                "ax1.grid(axis='y', alpha=0.3)\n",
                "\n",
                "# Plot 2: Node Expansions\n",
                "ax2.bar(df['Name'], df['Expansions'], color=['red', 'purple', 'blue'])\n",
                "ax2.set_title('Efficiency (Nodes Expanded)')\n",
                "ax2.set_ylabel('Count')\n",
                "ax2.grid(axis='y', alpha=0.3)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Visualize the Best Path (Manhattan)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Get Manhattan path (usually index 1)\n",
                "best_path = results[1]['Path']\n",
                "\n",
                "world.visualize(path=best_path, start=start, goal=goal, title=\"A* Path Found (Manhattan)\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write the notebook file
notebook_path = "notebooks/Auto_Lab_Report.ipynb"
with open(notebook_path, "w") as f:
    json.dump(notebook_content, f, indent=2)

print(f"✨ MAGIC DONE! ✨")
print(f"📁 Notebook created at: {notebook_path}")
print("🚀 Open it in Jupyter/VS Code and Run All Cells!")
