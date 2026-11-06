"""Presentación numérica de laboratorio: sin notación científica para residuos nulos."""

from aproxlab.ui.formatters import fmt_number


def test_fmt_number_treats_numerical_noise_as_zero() -> None:
    assert fmt_number(3.156e-16) == "0"
    assert fmt_number(-4.44e-16) == "0"
    assert fmt_number(0.0) == "0"


def test_fmt_number_uses_fixed_decimals_not_scientific() -> None:
    text = fmt_number(0.0003156)
    assert "e" not in text.lower()
    assert text.startswith("0.0003")


def test_fmt_number_keeps_ordinary_coefficients_readable() -> None:
    assert fmt_number(2.0) == "2"
    assert fmt_number(1.25) == "1.25"
    assert fmt_number(None) == "—"
