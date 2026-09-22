import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    output = ""
    try:
        curr_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(curr_directory, file_path))
        valid_target_path = os.path.commonpath([curr_directory, target_path]) == curr_directory


        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        ranProcess = subprocess.run(command, cwd=curr_directory, capture_output=True, text=True, timeout=30)

        if ranProcess.returncode != 0:
            output+= (f'Process exited with code {ranProcess.returncode}\n')

        if not ranProcess.stdout and not ranProcess.stderr:
            output+= ('No Output produced\n')

        if ranProcess.stdout:
            output+= (f'STDOUT: {ranProcess.stdout}\n')

        if ranProcess.stderr:
            output+= (f'STDERR: {ranProcess.stderr}\n')

        return output


    except Exception as e:
        return f"Error: executing Python file: {e}"
