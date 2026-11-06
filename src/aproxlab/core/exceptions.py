"""Errores de dominio del conjunto de datos y del ajuste."""


class DatasetError(ValueError):
    """Error recuperable relacionado con los pares (x, y)."""


class LengthMismatchError(DatasetError):
    """x e y no tienen la misma cantidad de elementos."""


class NonNumericDataError(DatasetError):
    """Algún valor no es numérico o no es finito."""


class InsufficientDataError(DatasetError):
    """No hay observaciones suficientes para el método solicitado."""


class DegenerateDesignError(DatasetError):
    """La matriz de diseño no permite un ajuste único (p. ej. x constante)."""
