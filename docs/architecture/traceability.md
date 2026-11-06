# Matriz de trazabilidad — Guía APE 04

| # | Requisito de la guía | Dónde se cumple |
|---|----------------------|-----------------|
| 1 | Calculadora con menú principal e ingreso de pares | `MainWindow` (menú/toolbar) + `DataView` |
| 2 | Validación: misma cantidad x/y, numéricos, n suficiente | `core/validation.py` + mensajes en DataView |
| 3 | Ajuste lineal: b0, b1, ecuación, SSE, SST, Syx, R², r | `core/regression/linear.py` + `core/metrics.py` + `LinearView` |
| 4 | Polinomio grado 2: a0,a1,a2, ecuación, ŷ, residuos, SSE | `core/regression/quadratic.py` + `QuadraticView` |
| 5 | Comparación de modelos y menor error | `core/comparison.py` + `ComparisonView` |
| 6 | Tres gráficas (lineal, cuadrático, comparativa) | `ui/views/charts_view.py` + Matplotlib |
| 7 | Diagrama de flujo general | `docs/flowcharts/01-general.md` |
| 8 | Diagramas por función (ingreso, lineal, cuadrático, errores, comparación, gráficas, menú) | `docs/flowcharts/02` … `08` |
| 9 | Programa organizado en funciones independientes alineadas a los flujos | módulos `core/` y `services/` con los mismos nombres de responsabilidad |
| 10 | Comprobar con un conjunto de datos y coherencia numérico-gráfica | `examples/` + pruebas canónicas + ejecución de la app |
| 11 | Analizar qué modelo es mejor y justificar | `ComparisonView` (SSE, R² ajustado, nota de anidamiento) + README |

Funcionalidades extra (no sustituyen lo obligatorio): CSV, exportar PNG, ejemplos, tema claro/oscuro, fórmulas.
