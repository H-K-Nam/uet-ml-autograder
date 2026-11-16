import time


def compute_mse(y_true, y_pred):
    # Intentional infinite loop to test timeout protection
    while True:
        time.sleep(1)


def fit_linear_regression(X, y):
    return None
