# Instruction

This is a simple CLI program to use ChatGPT.

## Prerequisites

1. Have an OpenAI API key. Refer to [OpenAI website](https://platform.openai.com/docs/overview) for more info.
2. Add balance in your account.
3. Store your API key to a safe place, for example, `~/.api_key_openai_1`. 
4. Add below line in your `~/.zshrc` or `~/.bashrc` (or other shell's equivalent).

```
export OPENAI_API_KEY="$(cat $HOME/.api_key_openai_1 2>/dev/null || echo '')"
```

## Usage

Do below if you use the program for the first time.

1. `git clone` this repo to your computer, then `cd` into your local repo.
2. Create a Python virtual environment for this repo, activate it, and 
do `pip install -r requirements.txt`
3. Make file `call_chatgpt_api.py` executable: `chmod u+x call_chatgpt_api.py`
4. Start the program by: `./call_chatgpt_api.py`; you can change model by 
adding `-m` argument, like: `./call_chatgpt_api.py -m "gpt-4.1"`; available
model names are on OpenAI website.
5. Type `exit` or `quit` in your prompt turn to stop the program.


