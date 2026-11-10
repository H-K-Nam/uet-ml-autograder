"""Unit tests for runner generator."""
from src.evaluator.runner_generator import generate_runner_code


def test_generate_runner_code():
    student_code = "def my_func(): return 42\n"
    test_code = "assert my_func() == 42\n"
    seed = 12345

    runner_code = generate_runner_code(student_code, test_code, random_seed=seed)

    assert f"random.seed({seed})" in runner_code
    assert f"np.random.seed({seed})" in runner_code
    assert "def my_func(): return 42" in runner_code
    assert "assert my_func() == 42" in runner_code
