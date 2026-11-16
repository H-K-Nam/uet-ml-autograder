"""Generates isolated runner script with seed injection and test assertions."""
from pathlib import Path


def generate_runner_code(
    extracted_student_code: str,
    test_code: str,
    random_seed: int = 42,
) -> str:
    """
    Wrap student code with seed injection and test verification into a single runner.
    """
    header = f"""# Auto-generated grading runner
import sys
import random
import numpy as np

# Seed injection for reproducibility
random.seed({random_seed})
np.random.seed({random_seed})

# ----------------- STUDENT SUBMISSION -----------------
"""
    middle = f"""
# ----------------- TEST VERIFICATION -----------------
"""
    return header + extracted_student_code + middle + test_code
