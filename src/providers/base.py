#!/usr/bin/env python3

"""
Abstract base class for LLM providers.

This module defines the interface that all LLM providers must implement,
ensuring consistency across different API implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All LLM provider implementations (ChatGPT, Claude, etc.) must inherit
    from this class and implement its abstract methods.
    """

    def __init__(self, model: str, api_key: Optional[str] = None):
        """
        Initialize the LLM provider.

        Parameters
        ----------
        model : str
            The model identifier to use for this provider.
        api_key : str, optional
            API key for authentication. If None, will attempt to read
            from environment variables.
        """
        self.model = model
        self.api_key = api_key
        self.messages: List[Dict[str, Any]] = []

    @abstractmethod
    def send_message(self, user_input: str, max_tokens: int = 1024, temperature: float = 0.5) -> str:
        """
        Send a message to the LLM and get a response.

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
            The LLM's response.
        """
        pass

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.messages = []

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the current conversation history.

        Returns
        -------
        List[Dict[str, Any]]
            The conversation history.
        """
        return self.messages.copy()

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of this provider.

        Returns
        -------
        str
            The provider name (e.g., "ChatGPT", "Claude").
        """
        pass
