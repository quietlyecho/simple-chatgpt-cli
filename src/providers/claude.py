#!/usr/bin/env python3

"""
Claude provider implementation.

This module provides an implementation of the LLM provider interface
for Anthropic's Claude API.
"""

import os
from typing import Optional
import anthropic

from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    """
    Claude provider implementation using Anthropic's API.
    """

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: Optional[str] = None):
        """
        Initialize the Claude provider.

        Parameters
        ----------
        model : str, optional
            The Claude model to use (default: "claude-sonnet-4-20250514").
        api_key : str, optional
            Anthropic API key. If None, reads from ANTHROPIC_API_KEY environment variable.
        """
        super().__init__(model, api_key)
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def send_message(self, user_input: str, max_tokens: int = 1024, temperature: float = 0.5) -> str:
        """
        Send a message to Claude and get a response.

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
            Claude's response.
        """
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        # Get response
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=self.messages
        )

        # Extract response content
        content = response.content[0].text

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
            "Claude"
        """
        return "Claude"
