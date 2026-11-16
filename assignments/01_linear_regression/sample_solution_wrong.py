import numpy as np


def compute_mse(y_true, y_pred):
    # Wrong implementation: returns sum of absolute errors instead of MSE
    return float(np.sum(np.abs(np.array(y_true) - np.array(y_pred))))


def fit_linear_regression(X, y):
    # Wrong implementation: returns zeros
    return np.zeros(X.shape[1] + 1)
