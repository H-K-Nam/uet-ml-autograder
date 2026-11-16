import numpy as np


def compute_mse(y_true, y_pred):
    return float(np.mean((np.array(y_true) - np.array(y_pred)) ** 2))


def fit_linear_regression(X, y):
    # Add bias column (ones)
    N = X.shape[0]
    X_b = np.hstack([np.ones((N, 1)), X])
    # Normal equation: w = (X^T X)^-1 X^T y
    w = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y
    return w
