#!/usr/bin/env python3

import argparse
import os
import threading
import time
import sys

from openai import OpenAI

EXIT_WORDS = ['exit', 'Exit', 'quit', 'Quit']


class ProcessSpinner:
    def __init__(self, message="Processing..."):
        self.spinning = False
        self.spinner_thread = None
        self.message = message
        
    def start(self):
        if self.spinning:
            return
        self.spinning = True
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
        
    def stop(self):
        self.spinning = False
        if self.spinner_thread:
            self.spinner_thread.join()
        # Clear the spinner line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
        
    def _spin(self):
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while self.spinning:
            sys.stdout.write(f'\r{spinner_chars[i % len(spinner_chars)]} {self.message}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str,
                    help="Name of the model to use",
                    default="gpt-4")  # Fixed default model name
args = parser.parse_args()

def stream_response(response_stream, spinner):
    """Stream response chunks to terminal."""
    full_content = ""
    first_content_received = False
    
    for chunk in response_stream:
        # Stop spinner when we get first actual content
        if not first_content_received and chunk.choices[0].delta.content is not None:
            spinner.stop()
            print("ChatGPT: ", end="", flush=True)
            first_content_received = True
            
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_content += content
    
    # If no content was received and spinner is still running, stop it
    if not first_content_received:
        spinner.stop()
        print("ChatGPT: ", end="", flush=True)
    
    print("\n######\n")
    return full_content

def start_chat(model: str):
    """
    Start a conversation with ChatGPT via API call.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Use standard OpenAI message format
    full_input = []

    while True:
        user_prompt = input("Prompt: ")

        if user_prompt in EXIT_WORDS:
            print("User ended conversation.")
            break

        # Add user message in standard format
        full_input.append({
            "role": "user",
            "content": user_prompt
        })

        spinner = ThinkingSpinner("Processing...")

        try:
            print()  # New line before spinner
            spinner.start()
            
            # All models use streaming with spinner
            response_stream = client.chat.completions.create(
                model=model,
                messages=full_input,
                stream=True
            )
            content = stream_response(response_stream, spinner)

            # Add assistant response to conversation history
            full_input.append({
                "role": "assistant", 
                "content": content
            })

        except Exception as e:
            spinner.stop()  # Always stop spinner on error
            print(f"Error: {e}")
            print("######\n")

if __name__ == '__main__':
    start_chat(model=args.model)