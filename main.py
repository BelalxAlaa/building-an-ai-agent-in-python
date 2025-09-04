import os
import sys

from dotenv import load_dotenv
from google.genai import Client, types

from functions.get_files_info import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error MSG: Prompt is not provided.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    is_verbose = "--verbose" in sys.argv

    if is_verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    generate_content(client, messages, is_verbose)


def generate_content(client: Client, messages: list[types.Content], is_verbose: bool):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls is None:
        print("No functions called")
        return
    
    for call in response.function_calls:
        print(f"Calling function: {call.name}({call.args})")


if __name__ == "__main__":
    main()
