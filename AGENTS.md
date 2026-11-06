# AGENTS.md — AproxLab

Reglas permanentes para agentes y colaboradores humanos. Este archivo tiene prioridad sobre hábitos genéricos cuando haya conflicto.

## Propósito

AproxLab es una aplicación de escritorio local (Python + PySide6) que calcula ajuste lineal por mínimos cuadrados y ajuste polinomial de grado 2, compara modelos y grafica resultados. Cumple la guía APE 04 de Métodos Numéricos y debe ser defendible en una entrevista de ingeniería de software.

## Prioridades

1. Correctitud matemática.
2. Cumplimiento íntegro de la guía académica.
3. Separación de responsabilidades (núcleo sin GUI).
4. Código limpio, tipado y testeable.
5. SOLID y patrones solo cuando resuelven un problema real.
6. Pruebas automatizadas del motor.
7. Interfaz clara, no ornamental.
8. Documentación alineada con el código (no afirmar lo que no existe).

## Arquitectura

- **Núcleo (`aproxlab.core`)**: validación, estrategias de regresión, métricas y comparación. Sin imports de PySide6 ni Matplotlib.
- **Modelos (`aproxlab.models`)**: DTOs inmutables (`Dataset`, resultados de ajuste y comparación).
- **Servicios (`aproxlab.services`)**: orquestación (análisis, CSV, ejemplos).
- **UI (`aproxlab.ui`)**: PySide6 en patrón MVP. Las vistas no calculan regresiones.
- **Gráficas**: Matplotlib embebido; el servicio de gráficos consume resultados del núcleo, no recalcula coeficientes.

Patrones aceptados en este repo:

- **MVP** para la GUI (Presenter/Controller coordina vistas y servicios).
- **Strategy** para algoritmos de ajuste (`LinearRegression`, `QuadraticRegression`).
- **Observer** vía señales/slots de Qt.
- **Simple Factory** (`create_strategy`) para instanciar estrategias por identificador.

No introducir Repository, DI containers, ni microservicios.

Detalle y justificación: `docs/architecture/decisions.md`.
Contrato Qt: `docs/QT_CONTRACT.md`.
Trazabilidad APE 04: `docs/architecture/traceability.md`.

## Convenciones de código

- Python 3.11+, PEP 8, type hints en APIs públicas.
- Identificadores en inglés; textos de UI y mensajes al usuario en español.
- Docstrings en módulos y clases del núcleo (Google style breve).
- Sin variables globales mutables. Sin magia numérica: constantes con nombre.
- No invertir matrices para resolver mínimos cuadrados; usar `numpy.linalg.lstsq` o `polyfit`.
- Errores de dominio: `aproxlab.core.exceptions.DatasetError` y subclases. No `print` en el núcleo.

## Pruebas (TDD en el núcleo)

- Toda función nueva del núcleo empieza con una prueba que falle por la funcionalidad ausente.
- Suite: `pytest` desde la raíz del repo.
- Tolerancias: `pytest.approx` con `rel=1e-9` o `abs=1e-9` salvo casos mal condicionados documentados.
- La GUI no es requisito para probar el motor. Evitar mocks del núcleo.

Casos canónicos de la guía:

- Lineal: `x=[0,1,2,3,4]`, `y=[1,3,5,7,9]` → pendiente 2, intercepto 1, SSE 0, R² 1, r 1.
- Cuadrático: `x=[0,1,2,3,4]`, `y=[1,2,5,10,17]` → `y = 1 + x²`.

## Calidad y verificación

Antes de dar por cerrado un cambio:

```text
python -m pytest
python -m ruff check src tests
python -m ruff format --check src tests
```

No afirmar que las pruebas pasan sin haber ejecutado `pytest` en esa misma sesión y leído la salida.

Si hay un fallo, investigar causa raíz antes de parchear (no “arreglos a ciegas”).

## GUI

- Qt Widgets (`QMainWindow`), no QML.
- Tema oscuro por defecto; claro opcional.
- Estados obligatorios: vacío, válido, inválido, éxito, error.
- Cálculos con n típico académico en el hilo de UI (ver contrato Qt). No bloquear con I/O innecesario.
- No botones decorativos sin acción.

## Git

- Commits pequeños por fase o por capacidad (núcleo, UI, docs).
- Mensajes en español o inglés, imperativo, explicando el porqué.
- No incluir secretos, `.venv` ni artefactos `dist/`.

## Fuera de alcance (YAGNI)

- Backend, API, base de datos, Electron/React.
- Modelos exponenciales/logarítmicos (la Strategy debe permitir añadirlos después, no implementarlos ahora).
- Autenticación, telemetría, actualizaciones automáticas.
