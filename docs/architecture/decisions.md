# Decisiones de arquitectura — AproxLab

## Por qué esta arquitectura

El sistema tiene dos mundos distintos: **álgebra de mínimos cuadrados** (debe ser correcta y testeable) y **una GUI de escritorio** (debe ser usable). Mezclarlos en una sola clase haría imposible defender el código en una entrevista y violaría el requisito académico de funciones independientes alineadas con los diagramas de flujo.

La estructura queda en capas planas, sin frameworks de inyección:

```text
UI (PySide6, MVP)
    → services (orquestación)
        → core (validación, Strategy de ajuste, métricas, comparación)
```

El núcleo no importa Qt ni Matplotlib. Eso garantiza que `pytest` cubra la guía sin levantar ventanas.

## Principios SOLID que sí aplican

- **SRP:** `LinearRegression` solo ajusta; `metrics.py` solo deriva SSE/SST/R²/r/Syx; las vistas solo pintan.
- **OCP:** un modelo nuevo (p. ej. exponencial) se añade como otra Strategy y entra a la comparación sin reescribir el Presenter.
- **LSP:** todas las estrategias exponen `fit(x, y) -> FitResult` con el mismo contrato (coeficientes de menor a mayor grado, `y_hat` alineado con x).
- **ISP:** el protocolo de Strategy tiene un solo método de ajuste más metadatos (`name`, `min_points`). No hay interfaz “DibujableYExportableYAjustable”.
- **DIP:** el Presenter depende de `AnalysisService` y del protocolo `RegressionStrategy`, no de widgets concretos para calcular.

No se crearon interfaces artificiales para rellenar un checklist.

## Patrones implementados (y por qué)

| Patrón | Dónde | Problema que resuelve |
|--------|-------|------------------------|
| **MVP** | `ui/` + `AnalysisPresenter` | Qt se acopla fácil a la lógica. El Presenter traduce eventos a casos de uso. |
| **Strategy** | `core/regression/` | Lineal y cuadrático son algoritmos intercambiables de “ajustar y devolver FitResult”. |
| **Simple Factory** | `create_strategy(kind)` | El servicio no instancia clases con `if` dispersos. |
| **Observer** | señales/slots Qt | Actualizar varias vistas tras un recálculo sin referencias cruzadas. |

## Alternativas descartadas

- **MVC clásico con modelo Qt observable para coeficientes:** excesivo; los resultados son un snapshot inmutable por cálculo.
- **VIPER / Clean Architecture con 15 carpetas:** sobreingeniería para ~dos algoritmos.
- **Repository:** no hay persistencia más allá de CSV opcional.
- **Invertir la matriz normal (`A.T @ A).I @ ...`:** inestable; se usa `lstsq` / `polyfit`.
- **QML:** la guía pide escritorio tipo laboratorio con tablas densas; Widgets encaja mejor.
- **Un único `QTableWidget` + funciones sueltas en `main.py`:** cumpliría el PDF, no el portafolio.

## Cómo se evitó la sobreingeniería

- Sin contenedor de DI: el `main` construye el grafo a mano (tres objetos).
- Sin hilos: n es pequeño; el contrato Qt lo documenta.
- Sin base de datos, sin plugins, sin bus de eventos propio.
- Métricas compartidas para ambos modelos (DRY) en lugar de copiar SSE en cada Strategy.

Si una función basta, se usa una función. Las clases existen donde hay estado o un contrato intercambiable.
