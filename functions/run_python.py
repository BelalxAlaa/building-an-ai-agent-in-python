import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", abs_file_path, *args], timeout=30, capture_output=True, text=True
        )
        if all((completed_process.stdout,completed_process.stderr)) :
            return "No output produced."

        formatted_output = f"""STDOUT:\n{completed_process.stdout}
STDERR:\n{completed_process.stderr}
{f"Process exited with code {completed_process.returncode}" if completed_process.returncode != 0 else ""}
"""

        return formatted_output

    except Exception as e:
        return f"Error: executing Python file: {e}"


if __name__ == "__main__":
    # run_python_file("calculator", "f.py")
    run_python_file("calculator", "tests.py")