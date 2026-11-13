"""Command Line Interface for UET ML Autograder."""
import sys
import shutil
import tempfile
from pathlib import Path
import click

from src.extractor import extract_code_from_notebook
from src.evaluator import generate_runner_code
from src.sandbox import DockerSandbox


@click.command()
@click.option(
    "--submission",
    "-s",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to student submission file (.py or .ipynb).",
)
@click.option(
    "--assignment",
    "-a",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Path to assignment directory containing tests and config.",
)
@click.option(
    "--local",
    is_flag=True,
    default=False,
    help="Run locally in subprocess instead of Docker (fallback mode).",
)
def main(submission: Path, assignment: Path, local: bool):
    """Grade a Machine Learning submission against assignment test suite."""
    click.echo(f"=== Grading Submission: {submission.name} ===")
    click.echo(f"Assignment Directory: {assignment}")

    # 1. Extract student code
    if submission.suffix == ".ipynb":
        student_code = extract_code_from_notebook(submission)
    elif submission.suffix == ".py":
        student_code = submission.read_text(encoding="utf-8")
    else:
        click.echo(f"Unsupported file extension: {submission.suffix}", err=True)
        sys.exit(1)

    # 2. Read assignment tests
    test_file = assignment / "tests" / "test_suite.py"
    if not test_file.exists():
        click.echo(f"Missing test file: {test_file}", err=True)
        sys.exit(1)
    test_code = test_file.read_text(encoding="utf-8")

    # 3. Generate combined runner
    runner_code = generate_runner_code(student_code, test_code)

    # 4. Prepare temporary staging directory
    temp_dir = Path(tempfile.mkdtemp(prefix="uet_grader_"))
    try:
        runner_path = temp_dir / "runner.py"
        runner_path.write_text(runner_code, encoding="utf-8")

        # Copy any auxiliary data files from assignment to temp_dir
        data_dir = assignment / "data"
        if data_dir.exists():
            shutil.copytree(data_dir, temp_dir / "data")

        # 5. Execute
        if local:
            click.echo("Running in local mode (subprocess)...")
            import subprocess
            proc = subprocess.run(
                [sys.executable, str(runner_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
            timeout = False
            oom = False
        else:
            click.echo("Running in Docker sandbox...")
            sandbox = DockerSandbox()
            result = sandbox.run_grading(temp_dir, runner_script="runner.py")
            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.exit_code
            timeout = result.timeout
            oom = result.oom_killed

        # 6. Report results
        click.echo("\n--- Execution Output ---")
        if stdout:
            click.echo(stdout.strip())
        if stderr:
            click.echo(f"Errors/Logs:\n{stderr.strip()}", err=True)

        click.echo("\n--- Final Verdict ---")
        if timeout:
            click.echo("Verdict: TIME LIMIT EXCEEDED (Timeout)")
        elif oom:
            click.echo("Verdict: MEMORY LIMIT EXCEEDED (OOM)")
        elif exit_code == 0:
            click.echo("Verdict: ALL TESTS PASSED (100/100)")
        else:
            click.echo(f"Verdict: FAILED (Exit Code {exit_code})")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
