import os
from .config import CHAR_LIMIT


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))



      
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(target_dir)
        return "\n".join(list(map(lambda filename: f"- {filename}: file_size={os.path.getsize(os.path.join(target_dir, filename))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, filename))}", contents)))
    except Exception as e:
        return f"Error: {e}"

    # abs_path_to_directory = os.path.abspath(os.path.join(working_directory,directory))

    # contents_of_dir = os.listdir(abs_path_to_directory)
    # print(f"contents_of_dir: {contents_of_dir}")
    # contents_formatted = list(map(lambda s: f'- {s}: file_size={os.path.getsize(os.path.abspath(os.path.join(working_directory, s)))} bytes, is_dir={os.path.isdir(os.path.getsize(os.path.abspath(os.path.join(working_directory, s))))}', contents_of_dir))
    # result = "\n".join(contents_formatted)

    # return result

    
def get_file_content(working_directory: str, file_path: str):


    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not  os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try: 
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(CHAR_LIMIT)
        return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: error raised {e}'
















    