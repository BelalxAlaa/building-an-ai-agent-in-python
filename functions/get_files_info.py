import os

from google.genai import types

from config import MAX_CHARS


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(target_dir)
        return "\n".join(
            list(
                map(
                    lambda filename: f"- {filename}: file_size={os.path.getsize(os.path.join(target_dir, filename))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, filename))}",
                    contents,
                )
            )
        )
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
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f"Error: error raised {e}"


def write_file(working_directory: str, file_path: str, content: str):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    try:
        # if not os.path.exists(abs_file_path):
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: error raised {e}"
        return f"Error: error raised {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the file content, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read from, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content provided to the file in the file path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written in the file",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    # description="Run the python file code given in the file path with the arguments given, constrained to the working directory.",
    description="Executes python file stated by the file path with the arguments given",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # "working_directory": types.Schema(
            #     type=types.Type.STRING,
            #     description="the working directory which the file belongs to.",
            # ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file path to the python file code to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="The operands you should do the calculations with."
                ),
                description="Optional extra arguments given for the program",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)
