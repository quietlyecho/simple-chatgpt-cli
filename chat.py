#!/usr/bin/env python3

"""
Unified chat interface for multiple LLM providers.

This module provides a command-line interface for conversing with different
LLM providers (ChatGPT, Claude) through a unified interface.
"""

import argparse
import sys
from src.config import ProviderFactory
from src.ui import ProcessSpinner

EXIT_WORDS = ['exit', 'Exit', 'quit', 'Quit']


def start_conversation(provider_name: str, model: str = None, max_tokens: int = 1024, temperature: float = 0.5):
    """
    Start an interactive conversation with the selected LLM provider.

    Parameters
    ----------
    provider_name : str
        Name of the provider to use ("chatgpt" or "claude").
    model : str, optional
        Model identifier. If None, uses the default model for the provider.
    max_tokens : int, optional
        Maximum number of tokens in responses (default: 1024).
    temperature : float, optional
        Sampling temperature (0.0 to 1.0). Higher values make output more random.
        Default is 0.5.
    """
    try:
        # Create provider instance
        provider = ProviderFactory.create_provider(provider_name, model=model)
        print(f"Starting conversation with {provider.get_provider_name()}.")
        print(f"Model: {provider.model}")
        print(f"Type 'exit' or 'quit' to end the conversation.\n")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing provider: {e}")
        print("Please check your API key is set in environment variables:")
        print(f"  - For ChatGPT: OPENAI_API_KEY")
        print(f"  - For Claude: ANTHROPIC_API_KEY")
        sys.exit(1)

    # Main conversation loop
    while True:
        try:
            user_input = input("Prompt: ")

            if user_input in EXIT_WORDS:
                print("Conversation ended.")
                break

            if not user_input.strip():
                continue

            # Show spinner while waiting for response
            spinner = ProcessSpinner("Processing...")
            print()  # New line before spinner
            spinner.start()

            try:
                # Get response from provider
                response = provider.send_message(user_input, max_tokens, temperature)

                # Stop spinner and display response
                spinner.stop()
                print(f"{provider.get_provider_name()}: {response}")
                print("######\n")

            except Exception as e:
                spinner.stop()
                print(f"Error getting response: {e}")
                print("######\n")

        except KeyboardInterrupt:
            print("\n\nConversation interrupted by user.")
            break
        except EOFError:
            print("\n\nConversation ended.")
            break


def main():
    """Main function to handle command line arguments and start the chat."""
    parser = argparse.ArgumentParser(
        description="Unified chat interface for LLM providers (ChatGPT, Claude)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --provider chatgpt
  %(prog)s --provider claude
  %(prog)s --provider chatgpt --model gpt-4o
  %(prog)s --provider claude --model claude-sonnet-4-20250514
  %(prog)s -p chatgpt -m gpt-4o --max-tokens 2048 --temperature 0.7

Supported providers:
  - chatgpt (default model: gpt-4o)
  - claude (default model: claude-sonnet-4-20250514)

Environment variables required:
  - OPENAI_API_KEY for ChatGPT
  - ANTHROPIC_API_KEY for Claude
        """
    )

    parser.add_argument(
        '-p', '--provider',
        type=str,
        required=True,
        choices=ProviderFactory.get_supported_providers(),
        help='LLM provider to use'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default=None,
        help='Model identifier (uses provider default if not specified)'
    )

    parser.add_argument(
        '--max-tokens',
        type=int,
        default=1024,
        help='Maximum tokens in response (default: 1024)'
    )

    parser.add_argument(
        '--temperature',
        type=float,
        default=0.5,
        help='Sampling temperature 0.0-1.0, higher is more random (default: 0.5)'
    )

    args = parser.parse_args()

    # Start conversation
    start_conversation(
        provider_name=args.provider,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature
    )


if __name__ == "__main__":
    main()
