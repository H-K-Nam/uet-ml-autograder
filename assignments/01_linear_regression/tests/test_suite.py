"""Test suite for Assignment 1: Linear Regression."""
import numpy as np


def run_tests():
    total_score = 0
    max_score = 100

    print("Running Test Suite for Linear Regression...")

    # --- Test 1: compute_mse (30 points) ---
    try:
        y_t = np.array([1.0, 2.0, 3.0, 4.0])
        y_p = np.array([1.0, 2.5, 2.5, 5.0])
        expected_mse = 0.375
        actual_mse = compute_mse(y_t, y_p)
        assert np.isclose(actual_mse, expected_mse, atol=1e-5), (
            f"Expected MSE {expected_mse}, got {actual_mse}"
        )
        total_score += 30
        print("[PASS] Test 1: compute_mse (+30/30)")
    except Exception as e:
        print(f"[FAIL] Test 1: compute_mse failed: {e}")

    # --- Test 2: fit_linear_regression on synthetic data (70 points) ---
    try:
        # Generate synthetic data with known w = [2.0, 3.5] (bias = 2.0, slope = 3.5)
        np.random.seed(42)
        X_train = np.linspace(0, 10, 50).reshape(-1, 1)
        y_train = 2.0 + 3.5 * X_train.ravel()

        w_hat = fit_linear_regression(X_train, y_train)
        expected_w = np.array([2.0, 3.5])

        assert w_hat.shape == (2,), f"Weight shape must be (2,), got {w_hat.shape}"
        assert np.allclose(w_hat, expected_w, atol=1e-4), (
            f"Expected weights {expected_w}, got {w_hat}"
        )
        total_score += 70
        print("[PASS] Test 2: fit_linear_regression (+70/70)")
    except Exception as e:
        print(f"[FAIL] Test 2: fit_linear_regression failed: {e}")

    print(f"\nFinal Score: {total_score}/{max_score}")
    if total_score < max_score:
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
