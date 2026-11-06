"""Solo se aceptan dígitos, signo y separador decimal (punto o coma)."""

from aproxlab.ui.widgets.numeric_delegate import is_allowed_number_text


def test_allows_digits_sign_and_decimal_separators() -> None:
    for text in ("", "-", "12", "12.5", "12,5", ".5", ",25", "-3,14", "0"):
        assert is_allowed_number_text(text)


def test_rejects_letters_and_extra_symbols() -> None:
    for text in ("12a", "e", "3.1.2", "1;2", "1 2", "x", "2e-3"):
        assert not is_allowed_number_text(text)
