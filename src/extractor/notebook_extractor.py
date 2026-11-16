"""Notebook code extractor module."""
from pathlib import Path
from typing import List, Optional
import nbformat


def extract_code_from_notebook(
    notebook_path: Path,
    target_tag: Optional[str] = "grade",
) -> str:
    """
    Extract executable Python code from code cells in a Jupyter Notebook.
    
    If target_tag is provided, only extracts cells tagged with target_tag.
    Otherwise, extracts all code cells while stripping IPython magics.
    """
    notebook = nbformat.read(str(notebook_path), as_version=4)
    extracted_lines: List[str] = []

    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue

        tags = cell.get("metadata", {}).get("tags", [])
        if target_tag and target_tag not in tags:
            # If tag filtering is enabled and tag not present, check for block comments
            if "# GRADE_CELL" not in cell.source and "# BEGIN SOLUTION" not in cell.source:
                continue

        # Filter out IPython magics (e.g., %matplotlib, !pip)
        cleaned_cell_lines = []
        for line in cell.source.splitlines():
            stripped = line.strip()
            if stripped.startswith(("%", "!")):
                cleaned_cell_lines.append(f"# [stripped magic] {line}")
            else:
                cleaned_cell_lines.append(line)

        extracted_lines.append("\n".join(cleaned_cell_lines))
        extracted_lines.append("\n# " + "=" * 40 + "\n")

    return "\n".join(extracted_lines)
