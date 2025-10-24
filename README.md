# Unified LLM Chat Interface

A simple CLI program to chat with multiple LLM providers (ChatGPT and Claude) through a unified interface.

## Features

- Unified interface for multiple LLM providers
- Support for ChatGPT (OpenAI) and Claude (Anthropic)
- Conversation history maintained throughout the session
- Spinner animation while waiting for responses
- Easy model selection
- Extensible architecture following software engineering best practices

## Architecture

The codebase follows industry-standard design patterns:

- **Strategy Pattern**: Abstract `LLMProvider` interface with concrete implementations
- **Factory Pattern**: `ProviderFactory` for instantiating providers
- **Separation of Concerns**: Clear separation between UI, business logic, and configuration
- **Single Responsibility Principle**: Each module has one clear purpose

```
api_chatgpt/
├── src/
│   ├── providers/       # LLM provider implementations
│   │   ├── base.py      # Abstract base provider
│   │   ├── chatgpt.py   # ChatGPT implementation
│   │   └── claude.py    # Claude implementation
│   ├── ui/              # UI components
│   │   └── spinner.py   # Processing spinner
│   └── config.py        # Provider factory and configuration
├── chat.py              # Unified CLI entry point
└── requirements.txt
```

## Prerequisites

### For ChatGPT

1. Have an OpenAI API key. Refer to [OpenAI website](https://platform.openai.com/docs/overview) for more info.
2. Add balance to your account.
3. Store your API key to a safe place, for example, `~/.api_key_openai_1`.
4. Add this line to your `~/.zshrc` or `~/.bashrc`:

```bash
export OPENAI_API_KEY="$(cat $HOME/.api_key_openai_1 2>/dev/null || echo '')"
```

### For Claude

1. Have an Anthropic API key. Refer to [Anthropic website](https://www.anthropic.com) for more info.
2. Add balance to your account.
3. Store your API key to a safe place, for example, `~/.api_key_anthropic_1`.
4. Add this line to your `~/.zshrc` or `~/.bashrc`:

```bash
export ANTHROPIC_API_KEY="$(cat $HOME/.api_key_anthropic_1 2>/dev/null || echo '')"
```

5. Remember to source the API keys: `source ~/.zshrc` or `source ~/.bashrc`

## Installation

1. Clone this repo to your computer, then `cd` into your local repo:
```bash
git clone <repo-url>
cd api_chatgpt
```

2. Create a Python virtual environment for this repo and activate it:
```bash
python3 -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make the chat program executable:
```bash
chmod u+x chat.py
```

## Usage

### Basic Usage

Chat with ChatGPT (default model: gpt-4o):
```bash
./chat.py --provider chatgpt
```

Chat with Claude (default model: claude-sonnet-4-20250514):
```bash
./chat.py --provider claude
```

### Advanced Usage

Specify a custom model:
```bash
./chat.py --provider chatgpt --model gpt-4o
./chat.py --provider claude --model claude-sonnet-4-20250514
```

Adjust maximum tokens:
```bash
./chat.py --provider chatgpt --max-tokens 2048
```

Adjust temperature (randomness):
```bash
./chat.py --provider chatgpt --temperature 0.7
./chat.py --provider claude --temperature 0.2  # More deterministic
./chat.py --provider chatgpt --temperature 1.0  # More creative
```

### Command-Line Options

```bash
./chat.py -h
```

Options:
- `-p, --provider` (required): Choose provider (`chatgpt` or `claude`)
- `-m, --model` (optional): Specify model name (uses provider default if not specified)
- `--max-tokens` (optional): Maximum tokens in response (default: 1024)
- `--temperature` (optional): Sampling temperature 0.0-1.0, higher is more random (default: 0.5)

### During Conversation

- Type your prompts and press Enter to send
- Type `exit` or `quit` to end the conversation
- Press Ctrl+C to interrupt the conversation

## Extending the System

To add a new LLM provider:

1. Create a new provider class in `src/providers/` that inherits from `LLMProvider`
2. Implement the required abstract methods: `send_message()` and `get_provider_name()`
3. Register the provider in `src/config.py` in the `ProviderFactory.PROVIDERS` dictionary

## License

See LICENSE file for details.


