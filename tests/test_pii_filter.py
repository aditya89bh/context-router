from context_router.context.pii_filter import sanitize_text


def test_sanitize_text_redacts_email_addresses() -> None:
    assert sanitize_text("Contact ops@example.com for details") == "Contact [REDACTED_EMAIL] for details"


def test_sanitize_text_redacts_phone_numbers() -> None:
    assert sanitize_text("Escalate to +1 (415) 555-0199 today") == "Escalate to [REDACTED_PHONE] today"


def test_sanitize_text_redacts_api_key_like_values() -> None:
    assert sanitize_text("api_key=abcd1234abcd1234abcd") == "[REDACTED_SECRET]"
    assert sanitize_text("token: abcdefghijklmnop1234") == "[REDACTED_SECRET]"


def test_sanitize_text_leaves_enterprise_context_without_pii_unchanged() -> None:
    text = "Review deployment readiness and incident response ownership."
    assert sanitize_text(text) == text
