import os
import sys

from dotenv import load_dotenv
from google.genai import Client, types

from config import AGENT_TOOLS, SYSTEM_PROMPT
from functions import get_file_content, get_files_info, run_python_file, write_file

functions_mapping = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


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

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        ),
    ]

    for _ in range(20):
        try:
            response = generate_content(client, messages, is_verbose)

            if not response.function_calls:
                print(response.text)
                break

        except Exception as e:
            print(f"Error: {e}")


def call_function(
    function_call_part: types.FunctionCall,
    verbose: bool = False,
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name not in functions_mapping:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    result = functions_mapping[function_call_part.name](
        working_directory="./calculator", **function_call_part.args
    )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )


def generate_content(
    client: Client,
    messages: list[types.Content],
    is_verbose: bool,
) -> types.GenerateContentResponse:
    # Loop
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[AGENT_TOOLS],
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls is None:
        print("No functions called")
        return response

    for candidate in response.candidates:
        messages.append(candidate.content)

    for call in response.function_calls:
        call_result = call_function(call, is_verbose)
        if not call_result.parts[0].function_response.response:
            raise Exception("Fatal Exception")

        if call_result.parts[0].function_response.response and is_verbose:
            print(f"-> {call_result.parts[0].function_response.response}")

        messages.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=call_result.parts[0].function_response.response["result"]
                    )
                ],
            )
        )
        # messages.append(call_result)

        return response


if __name__ == "__main__":
    main()
