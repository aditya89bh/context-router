"""Lightweight helpers for consistent API deprecation warnings."""
from __future__ import annotations

import functools
import warnings
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def deprecation_message(name: str, replacement: str | None = None, remove_in: str | None = None) -> str:
    """Build a standard deprecation warning message."""
    message = f"{name} is deprecated"
    if replacement:
        message += f"; use {replacement} instead"
    if remove_in:
        message += f"; scheduled for removal in {remove_in}"
    return message


def warn_deprecated(name: str, replacement: str | None = None, remove_in: str | None = None, stacklevel: int = 2) -> None:
    """Emit a DeprecationWarning with a consistent message."""
    warnings.warn(
        deprecation_message(name=name, replacement=replacement, remove_in=remove_in),
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def deprecated(name: str | None = None, replacement: str | None = None, remove_in: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorate a callable so using it emits a DeprecationWarning."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        deprecated_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            warn_deprecated(deprecated_name, replacement=replacement, remove_in=remove_in, stacklevel=3)
            return func(*args, **kwargs)

        return wrapper

    return decorator
