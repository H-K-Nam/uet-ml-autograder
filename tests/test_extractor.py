"""Unit tests for notebook extractor."""
from pathlib import Path
import nbformat as nbf
import pytest

from src.extractor.notebook_extractor import extract_code_from_notebook


def test_extract_code_from_notebook(tmp_path: Path):
    nb = nbf.v4.new_notebook()
    # Cell 1: Non-grade cell with IPython magic
    cell1 = nbf.v4.new_code_cell("%matplotlib inline\nx = 10")
    # Cell 2: Grade cell with tag comment
    cell2 = nbf.v4.new_code_cell("# GRADE_CELL\ndef add(a, b):\n    return a + b")
    nb.cells = [cell1, cell2]

    nb_file = tmp_path / "test_nb.ipynb"
    with open(nb_file, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    extracted = extract_code_from_notebook(nb_file)
    assert "def add(a, b):" in extracted
    assert "%matplotlib" not in extracted
    assert "x = 10" not in extracted
