import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        curr_directory = os.path.abspath(working_directory)
        target_directory = os.path.abspath(os.path.join(curr_directory, directory))
        valid_target_dir = os.path.commonpath([curr_directory, target_directory]) == curr_directory

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        else:
            entries = []
            for name in os.listdir(target_directory):
                entry_path = os.path.join(target_directory, name)
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                entries.append(
                    f"Success: {name}: file_size={size} bytes, is_dir={is_dir}"
                )
            return "\n".join(entries)

    except OSError as e:
        return f"Error: {e}"
