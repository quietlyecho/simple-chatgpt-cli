#!/usr/bin/env python3

"""
Configuration and factory for LLM providers.

This module provides a factory pattern implementation for creating
LLM provider instances based on user choice.
"""

from typing import Optional
from .providers import LLMProvider, ChatGPTProvider, ClaudeProvider


class ProviderFactory:
    """
    Factory class for creating LLM provider instances.

    This factory implements the Factory Pattern to instantiate the
    appropriate LLM provider based on user selection.
    """

    # Supported providers and their default models
    PROVIDERS = {
        "chatgpt": {
            "class": ChatGPTProvider,
            "default_model": "gpt-5"
        },
        "claude": {
            "class": ClaudeProvider,
            "default_model": "claude-sonnet-4-5-20250929" 
        }
    }

    @classmethod
    def create_provider(
        cls,
        provider_name: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> LLMProvider:
        """
        Create an LLM provider instance.

        Parameters
        ----------
        provider_name : str
            Name of the provider ("chatgpt" or "claude").
        model : str, optional
            Model identifier. If None, uses the default model for the provider.
        api_key : str, optional
            API key for authentication. If None, reads from environment variables.

        Returns
        -------
        LLMProvider
            An instance of the requested provider.

        Raises
        ------
        ValueError
            If the provider name is not supported.
        """
        provider_name = provider_name.lower()

        if provider_name not in cls.PROVIDERS:
            supported = ", ".join(cls.PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: {provider_name}. "
                f"Supported providers: {supported}"
            )

        provider_config = cls.PROVIDERS[provider_name]
        provider_class = provider_config["class"]
        default_model = provider_config["default_model"]

        # Use provided model or default
        model_to_use = model if model else default_model

        return provider_class(model=model_to_use, api_key=api_key)

    @classmethod
    def get_supported_providers(cls) -> list:
        """
        Get a list of supported provider names.

        Returns
        -------
        list
            List of supported provider names.
        """
        return list(cls.PROVIDERS.keys())

    @classmethod
    def get_default_model(cls, provider_name: str) -> str:
        """
        Get the default model for a provider.

        Parameters
        ----------
        provider_name : str
            Name of the provider.

        Returns
        -------
        str
            The default model identifier.

        Raises
        ------
        ValueError
            If the provider name is not supported.
        """
        provider_name = provider_name.lower()
        if provider_name not in cls.PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider_name}")

        return cls.PROVIDERS[provider_name]["default_model"]
