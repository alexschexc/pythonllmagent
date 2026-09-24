import os
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Takes input as a string called content and writes it to file specified by the file_path, if it exists and/or is reachable, otherwise prints errors appropriate to what is not true.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "provided path to file that is intended to have content written into it",
                },
                "content": {
                    "type": "string",
                    "description": "provided content string that is written to the file.",
                },
            },
            "required":["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        curr_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(curr_directory, file_path))
        valid_target_path = os.path.commonpath([curr_directory, target_path]) == curr_directory


        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory.'

        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except OSError as e:
        return f"Error: {e}"
