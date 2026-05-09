"""Compatibility module exposing the application configuration.

This module exists so existing imports can continue to use
`app.core.config.config` while the actual implementation lives in
`app.core.settings`.
"""

from .settings import config

__all__ = ["config"]
