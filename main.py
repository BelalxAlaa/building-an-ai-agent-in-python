import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error MSG: Prompt is not provided.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    is_verbose = '--verbose' in sys.argv

    if is_verbose:
        print(f"User prompt: {user_prompt}")
    

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]


    generate_content(client, messages, is_verbose)
    

def generate_content(client, messages, is_verbose):

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")
    


if __name__ == "__main__":
    main()
