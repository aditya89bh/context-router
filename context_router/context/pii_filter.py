"""Small PII redaction helpers for text utilities."""
from __future__ import annotations

import re

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)")
API_KEY_RE = re.compile(r"\b(?:api[_-]?key|token|secret)[=:]\s*['\"]?[A-Za-z0-9_\-]{16,}['\"]?", re.IGNORECASE)


def sanitize_text(text: str) -> str:
    """Return text with common email, phone, and API-key-like values redacted."""
    sanitized = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    sanitized = PHONE_RE.sub("[REDACTED_PHONE]", sanitized)
    return API_KEY_RE.sub("[REDACTED_SECRET]", sanitized)
