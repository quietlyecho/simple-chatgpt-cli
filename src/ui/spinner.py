#!/usr/bin/env python3

"""
Spinner UI component for showing processing status.

This module provides a spinner that displays while waiting for LLM responses.
"""

import sys
import threading
import time


class ProcessSpinner:
    """
    A simple spinner to show processing status.

    This spinner runs in a separate thread and displays an animated
    spinner character while processing is ongoing.
    """

    def __init__(self, message: str = "Processing..."):
        """
        Initialize the spinner.

        Parameters
        ----------
        message : str, optional
            The message to display alongside the spinner (default: "Processing...").
        """
        self.spinning = False
        self.spinner_thread = None
        self.message = message

    def start(self) -> None:
        """Start the spinner animation."""
        if self.spinning:
            return
        self.spinning = True
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self) -> None:
        """Stop the spinner animation and clear the line."""
        self.spinning = False
        if self.spinner_thread:
            self.spinner_thread.join()
        # Clear the spinner line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()

    def _spin(self) -> None:
        """
        Internal method that runs the spinner animation.

        This runs in a separate thread and updates the spinner character
        at regular intervals.
        """
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while self.spinning:
            sys.stdout.write(f'\r{spinner_chars[i % len(spinner_chars)]} {self.message}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
