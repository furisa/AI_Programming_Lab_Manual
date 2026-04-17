import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn import datasets
import os

def test_numpy():
    print("\n****Testing NumPy...****")
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"Array shape: {arr.shape}")
    print(f"NumPy version: {np.__version__}")
    return True

def test_pandas():
    print("\n****Testing Pandas...****")
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
    print(f"DataFrame shape: {df.shape}")
    print(f"Pandas version: {pd.__version__}")
    return True

def test_matplotlib():
    print("\n****Testing Matplotlib...****")
    plt.figure(figsize=(4, 3))
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.title("Test Plot")
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    plt.savefig("outputs/test_plot.png")
    plt.close()
    print(f"Matplotlib version: {plt.matplotlib.__version__}")
    return True

def test_sklearn():
    print("\n****Testing scikit-learn...****")
    iris = datasets.load_iris()
    print(f"Iris dataset shape: {iris.data.shape}")
    print(f"scikit-learn version: {sklearn.__version__}")
    return True

def main():
    print("=" * 50)
    print("AI Environment Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    tests = [test_numpy(), test_pandas(), test_matplotlib(), test_sklearn()]
    print("\n" + "=" * 50)
    if all(tests):
        print("ALL TESTS PASSED!")
    else:
        print("Some tests failed.")
    print("=" * 50)

if __name__ == "__main__":
    main()