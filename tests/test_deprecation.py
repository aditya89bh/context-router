import warnings

from context_router.deprecation import deprecated, deprecation_message, warn_deprecated


def test_deprecation_message_includes_replacement_and_removal() -> None:
    assert deprecation_message("old_api", replacement="new_api", remove_in="1.0") == "old_api is deprecated; use new_api instead; scheduled for removal in 1.0"


def test_warn_deprecated_emits_deprecation_warning() -> None:
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        warn_deprecated("old_api", replacement="new_api")

    assert len(captured) == 1
    assert captured[0].category is DeprecationWarning
    assert "use new_api instead" in str(captured[0].message)


def test_deprecated_decorator_preserves_behavior_and_warns() -> None:
    @deprecated(replacement="new_function", remove_in="1.0")
    def old_function(value: int) -> int:
        return value + 1

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        result = old_function(1)

    assert result == 2
    assert captured[0].category is DeprecationWarning
    assert "old_function is deprecated" in str(captured[0].message)
