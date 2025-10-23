#!/usr/bin/env python3

"""
ChatGPT provider implementation.

This module provides an implementation of the LLM provider interface
for OpenAI's ChatGPT API.
"""

import os
from typing import Optional
from openai import OpenAI

from .base import LLMProvider


class ChatGPTProvider(LLMProvider):
    """
    ChatGPT provider implementation using OpenAI's API.
    """

    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize the ChatGPT provider.

        Parameters
        ----------
        model : str, optional
            The OpenAI model to use (default: "gpt-4o").
        api_key : str, optional
            OpenAI API key. If None, reads from OPENAI_API_KEY environment variable.
        """
        super().__init__(model, api_key)
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def send_message(self, user_input: str, max_tokens: int = 1024, temperature: float = 0.5) -> str:
        """
        Send a message to ChatGPT and get a response.

        Parameters
        ----------
        user_input : str
            The user's message.
        max_tokens : int, optional
            Maximum number of tokens in the response.
        temperature : float, optional
            Sampling temperature (0.0 to 1.0). Higher values make output more random.
            Default is 0.5.

        Returns
        -------
        str
            ChatGPT's response.
        """
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        # Get response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Extract response content
        content = response.choices[0].message.content

        # Add assistant response to history
        self.messages.append({
            "role": "assistant",
            "content": content
        })

        return content

    def get_provider_name(self) -> str:
        """
        Get the name of this provider.

        Returns
        -------
        str
            "ChatGPT"
        """
        return "ChatGPT"
