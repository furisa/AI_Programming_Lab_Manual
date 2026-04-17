"""Utility functions for reproducibility."""
import random
import numpy as np

def set_seed(seed=42):
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    print(f"Random seed set to {seed}")