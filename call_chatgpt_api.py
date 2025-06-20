import os

from openai import OpenAI

EXIT_WORDS = ['exit', 'Exit', 'quit', 'Quit']

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
        model="gpt-4.1",
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

