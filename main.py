import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from available_functions import available_functions
from available_functions import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt,},
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if response is None:
        raise RuntimeError("LLM Response object empty.")




    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call=tool_call, verbose=args.verbose)
            if not result_message["content"]:
                raise Exception("Error: tool call has no content")
            if args.verbose:
                print(f"-> {result_message['content']}")

    else:
        #no tools requested
        print(message.content)

if __name__ == "__main__":
    main()
