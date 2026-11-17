# Contrato Qt — AproxLab

Fuente de verdad para la GUI. Cualquier cambio de ventana, estado o hilos debe actualizar este archivo.

## Estructura de ventana

- **Contenedor:** `QMainWindow` (`aproxlab.ui.main_window.MainWindow`).
- **Por qué:** menú, barra de herramientas y un banco de trabajo (datos + resultados + gráficas a la vez).
- **No usar:** QML/Qt Quick, `QDialog` como ventana principal, posicionamiento absoluto.

## Árbol de composición

```text
MainWindow
├── MenuBar (Archivo, Ejemplos, Ver, Ayuda)
├── ToolBar (ejemplos, Limpiar, ocultar/mostrar gráficas)
├── StatusBar (n, SSE, ganador)
└── QSplitter horizontal
    ├── DataView (tabla x,y, agregar/eliminar fila, Limpiar, Ajustar/F5)
    └── QSplitter vertical
        ├── QTabWidget: Lineal | Cuadrático | Comparación
        │   └── QuadraticView: ocultar/mostrar cálculo de la matriz
        └── ChartsView (Recta | Parábola | Ambos)
```

## Propiedad del estado

| Estado | Dueño | Lectores |
|--------|--------|----------|
| Pares (x, y) editables | `DatasetTableModel` | DataView; MainWindow los entrega al Presenter al ajustar |
| Resultado lineal / cuadrático | `AnalysisPresenter` (último `AnalysisReport`) | vistas de resultados y gráficas |
| Tema claro/oscuro | `MainWindow._theme` + `apply_theme` | aplicación, fórmulas y gráficas |
| Mensaje de error de validación | `MainWindow._on_failed`, desde lectura de tabla o señal `analysis_failed` del Presenter | StatusBar + DataView |
| Visibilidad del cálculo de la matriz | `QuadraticView` | botón y contenedor de ecuaciones, matriz y Gauss-Jordan |
| Visibilidad de gráficas | `MainWindow` | botón de toolbar y splitter vertical |

Flujo: acción de usuario → señal de vista → Presenter → `AnalysisService` (núcleo) → señal `analysis_ready` / `analysis_failed` → vistas se refrescan. Las vistas **no** se conectan entre sí.

La ventana arranca cargando y calculando **Datos de clase**. Editar la tabla no recalcula automáticamente: se usa **Ajustar / F5**. Seleccionar un ejemplo sí dispara el análisis.

**Limpiar** está disponible en Datos, la toolbar y Archivo. Las tres entradas ejecutan `MainWindow._clear_workspace`: reinician el selector de ejemplos sin cargar otro conjunto, dejan cinco filas vacías (`n = 0`), borran mensajes, tablas, fórmulas numéricas, pasos de Gauss-Jordan, comparación, gráficas y `AnalysisPresenter.last_report`. Las ecuaciones genéricas y los títulos permanecen como orientación. El estado final de la barra es `n=0 · sin ajuste`; no queda reporte para exportar.

El botón **Ocultar / Mostrar cálculo de la matriz** solo cambia la visibilidad del bloque de ecuaciones normales, matriz aumentada y operaciones de Gauss-Jordan. No recalcula ni borra datos. Sumatorias, coeficientes, errores e indicadores siguen visibles. Se deshabilita sin cálculo y se habilita al recibir un resultado cuadrático; conserva la preferencia de visibilidad al limpiar y cargar otro conjunto. Limpiar también conserva el tema y la visibilidad de gráficas.

## Modelo de hilos

Los ajustes con n académico (decenas o cientos de puntos) son O(n) y se ejecutan en el **hilo de UI**.

No hay `QThread` en la versión actual. Si en el futuro se importan CSV masivos, el worker se llamaría `AnalysisWorker` y emitiría `finished(AnalysisReport)` / `failed(str)` hacia el Presenter. Hasta entonces, YAGNI.

## Estados por superficie

| Superficie | Vacío | Inválido | Válido / éxito | Error |
|------------|-------|----------|----------------|-------|
| DataView | filas vacías, `n = 0`; agregar fila o cargar ejemplo | mensaje sobre la tabla (no numérico, fila incompleta, n insuficiente) | tabla editable | igual que inválido |
| LinearView / QuadraticView | ecuaciones genéricas, tablas vacías y tarjetas sin valores | error en Datos y StatusBar | desarrollo paso a paso y ecuación ajustada | error en Datos y StatusBar |
| ComparisonView | sin ajuste, indicadores sin valores y tabla vacía tras limpiar | — | tabla SSE/SST/Syx/R², reducción SSE y conclusión | — |
| ChartsView | canvas sin puntos, curvas ni leyenda tras limpiar | — | tres gráficas con ejes, título y leyenda; diálogos para ampliarlas | — |

Un error de validación muestra el mensaje; no borra automáticamente las vistas del ajuste anterior. **Limpiar** permite volver al estado vacío desde éxito o error.

No hay estado de red. “Busy” no aplica: el cálculo es inmediato.

## Señales semánticas

- `DataView.fit_requested()`
- `DataView.clear_requested()`
- `AnalysisPresenter.analysis_ready(report)`
- `AnalysisPresenter.analysis_failed(message)`
- `AnalysisPresenter.dataset_loaded(x, y, label)`

## Teclado y redimensionado

- Layouts (`QHBoxLayout` / `QVBoxLayout` / `QGridLayout`) desde el inicio; tamaño mínimo 1080×680.
- Controles de Datos en el orden del layout: tabla → agregar/eliminar/limpiar → ajustar. F5 ejecuta el ajuste; pestañas y controles admiten navegación de teclado de Qt.
