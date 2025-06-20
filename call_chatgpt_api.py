import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

user_input = input("Prompt: ")

response = client.responses.create(
    model="gpt-4.1",
    input=user_input
)

print(response.output_text)
