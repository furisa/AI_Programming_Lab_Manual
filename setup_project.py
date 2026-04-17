import os
target_path = os.getcwd()
project_name = "heuristic-search-lab"
full_path = os.path.join(target_path, project_name)
folders = ["src", "experiments", "tests", "results", "results/data", "results/figures"]
for f in folders: os.makedirs(os.path.join(full_path, f), exist_ok=True)

files = {
    "requirements.txt": "numpy\nmatplotlib",
    "src/grid_world.py": "class GridWorld: pass",
    "experiments/run_all_experiments.py": "print('Hello World')"
}
for name, content in files.items():
    with open(os.path.join(full_path, name), "w") as f: f.write(content)

print("✅ Setup Done! Files created in AI_Programming_Lab_Manual")
