import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "returns file contents, as a string, up to MAX_CHARS in size. If size is achieved, truncation warning is appended to the output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to file to be read from",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        curr_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(curr_directory, file_path))
        valid_target_path = os.path.commonpath([curr_directory, target_path]) == curr_directory


        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            extra = f.read(1)

        if extra:
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content


    except OSError as e:
        return f"Error: {e}"
