"""Shared app configuration helpers."""

import os


def cors_origins() -> list[str]:
    """CORS allow-list from CORS_ORIGINS (comma-separated).

    Defaults to "*" for local development. Set this to the frontend origin
    when hosting the API separately.
    """
    raw = os.getenv("CORS_ORIGINS", "*")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]
