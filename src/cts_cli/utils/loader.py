# -*- coding: utf-8 -*-
"""Loader wrapper."""
import sys
from threading import Thread
from itertools import cycle
from time import sleep
from os import get_terminal_size


class Loader:
    """
    A utility class for displaying a loading animation.

    The Loader class provides methods to start and stop the loading animation,
    as well as a decorator to wrap a function with the Loader context manager.

    Args:
        desc: The description of the loading process. Defaults to "Loading...".
        end: The string to be displayed at the end of the loading process.
        Defaults to an empty string.
        timeout: The time interval between each animation frame. Defaults to 0.1 seconds.

    Attributes:
        desc: The description of the loading process.
        end: The string to be displayed at the end of the loading process.
        timeout: The time interval between each animation frame.
        steps: The set of steps used for the loading animation.
        done: A flag indicating whether the loading animation is done.

    Methods:
        start: Starts the loading animation.
        stop: Stops the loading animation.
        __call__: Decorator that wraps a function with the Loader context manager.
        __enter__: Enters the Loader context.
        __exit__: Exits the Loader context.

    """

    def __init__(self, desc="Loading...", end="", timeout=0.07):
        """
        Initializes the Loader object.

        Args:
            desc: The description of the loading process. Defaults to "Loading...".
            end: The string to be displayed at the end of the loading process.
            Defaults to an empty string.
            timeout: The time interval between each animation frame. Defaults to 0.1 seconds.

        Returns:
            None
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["◢", "◣", "◤", "◥"]
        self.done = False

    def start(self):
        """
        Starts the loading animation in a separate thread.

        Returns:
            None
        """
        self._thread.start()

    def _animate(self):
        """
        Animates the loading process by cycling through a set of steps.

        Returns:
            None
        """
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def stop(self):
        """
        Stops the loading animation and clears the loading message from the terminal.

        Returns:
            None
        """
        if sys.stdout.isatty():  # Check if running in a terminal
            cols = get_terminal_size((80, 20)).columns
            print("\r" + " " * cols, end="", flush=True)
            print(f"\r{self.end}", flush=True)

    def __call__(self, func):
        """
        Decorator that wraps a function with the Loader context manager.

        Args:
            func: The function to be wrapped.

        Returns:
            The wrapped function.
        """

        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    def __enter__(self):
        """
        Enters the Loader context.

        Returns:
            None
        """
        self.start()

    def __exit__(self, exc_type, exc_value, tb):
        """
        Exits the Loader context and stops the loading animation.

        Args:
            exc_type: The type of the exception raised, if any.
            exc_value: The value of the exception raised, if any.
            tb: The traceback object associated with the exception, if any.

        Returns:
            None
        """
        self.stop()
