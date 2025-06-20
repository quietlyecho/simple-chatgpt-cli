#!/usr/bin/env python3

import argparse
import os

from openai import OpenAI

EXIT_WORDS = ['exit', 'Exit', 'quit', 'Quit']

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str,
                    help="Name of the model to use",
                    default="gpt-4.1")
args = parser.parse_args()

def start_chat(model: str):
    """
    Start a conversation with ChatGPT via API call.
    """

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    full_input = []

    while True:
        user_prompt = input("Prompt: ")
        print('######\n')

        if user_prompt in EXIT_WORDS:
            print("User ended conversation.")
            break

        full_input.append(
            {
                "role": "user",
                "content": [
                    {"type": "input_text",
                     "text": user_prompt},
                ]
            }
        )

        response = client.responses.create(
            model=model,
            input=full_input
        )
        print(f'ChatGPT: {response.output_text}\n######\n')

        response_msg = {
            "role": "assistant",
            "content": [
                {"type": "output_text",
                 "text": response.output_text}
            ]
        }
        full_input.append(response_msg)

if __name__ == '__main__':
    start_chat(
        model=args.model
    )
