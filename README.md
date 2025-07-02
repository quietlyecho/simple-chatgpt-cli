# Instruction

This is a simple CLI for using ChatGPT.

## Prerequisites

1. Have an OpenAI API key. Refer to [OpenAI website](https://platform.openai.com/docs/overview) for more info.
2. Add balance in your account.
3. Store your API key to a safe place, for example, `~/.api_key_openai_1`. 
4. Add below line in your `~/.zshrc` or `~/.bashrc` (or other shell's equivalent).

```
export OPENAI_API_KEY="$(cat $HOME/.api_key_openai_1 2>/dev/null || echo '')"
```

## Usage

1. Make file `call_chatgpt_api.py` executable by running: `chmod u+x call_chatgpt_api.py`
2. Start the program by running: `./call_chatgpt_api.py`
3. You can change model by running: `./call_chatgpt_api.py -m gpt-4.1`; available
model names are on OpenAI website.
