"""Importación y exportación de CSV y reportes de texto."""

from __future__ import annotations

import csv
from pathlib import Path

from aproxlab.core.exceptions import NonNumericDataError
from aproxlab.services.analysis import AnalysisReport


def load_xy_csv(path: str | Path) -> tuple[list[float], list[float]]:
    """Lee un CSV con columnas x,y (cabecera opcional)."""
    file_path = Path(path)
    x_values: list[float] = []
    y_values: list[float] = []
    with file_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        for row_number, raw in enumerate(reader, start=1):
            if not raw or all(not cell.strip() for cell in raw):
                continue
            if len(raw) < 2:
                raise NonNumericDataError(f"La fila {row_number} no tiene dos columnas.")
            if row_number == 1 and _is_header(raw[0], raw[1]):
                continue
            x_values.append(_parse_cell(raw[0], row_number, "x"))
            y_values.append(_parse_cell(raw[1], row_number, "y"))
    return x_values, y_values


def export_xy_csv(path: str | Path, x: list[float], y: list[float]) -> None:
    """Escribe pares x,y con cabecera."""
    file_path = Path(path)
    with file_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["x", "y"])
        for xi, yi in zip(x, y, strict=True):
            writer.writerow([xi, yi])


def export_report_text(path: str | Path, report: AnalysisReport) -> None:
    """Exporta un resumen legible del análisis."""
    file_path = Path(path)
    lines = [
        "AproxLab — reporte de aproximación funcional",
        "",
        f"Observaciones: {report.x.size}",
        "",
        "Ajuste lineal",
        f"  Ecuación: {report.linear.equation}",
        f"  a0 (intersección): {report.linear.coefficients[0]}",
        f"  a1 (pendiente): {report.linear.coefficients[1]}",
        f"  SSE: {report.linear_metrics.sse}",
        f"  SST: {report.linear_metrics.sst}",
        f"  Syx: {report.linear_metrics.std_error}",
        f"  R²: {report.linear_metrics.r_squared}",
        f"  r: {report.linear_metrics.correlation}",
        "",
        "Ajuste cuadrático",
        f"  Ecuación: {report.quadratic.equation}",
        f"  a0, a1, a2: {list(report.quadratic.coefficients)}",
        f"  SSE: {report.quadratic_metrics.sse}",
        "",
        "Comparación",
        f"  Criterio: {report.comparison.criterion}",
        f"  Mejor ajuste (menor error): {report.comparison.winner_name}",
        f"  Nota: {report.comparison.caution}",
        "",
    ]
    file_path.write_text("\n".join(lines), encoding="utf-8")


def _is_header(first: str, second: str) -> bool:
    try:
        float(first.replace(",", "."))
        float(second.replace(",", "."))
    except ValueError:
        return True
    return False


def _parse_cell(raw: str, row_number: int, axis: str) -> float:
    text = raw.strip().replace(",", ".")
    try:
        return float(text)
    except ValueError as exc:
        raise NonNumericDataError(
            f"Valor no numérico en {axis} (fila {row_number}): '{raw}'."
        ) from exc
