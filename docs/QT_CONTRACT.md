# Contrato Qt — AproxLab

Fuente de verdad para la GUI. Cualquier cambio de ventana, estado o hilos debe actualizar este archivo.

## Estructura de ventana

- **Contenedor:** `QMainWindow` (`aproxlab.ui.main_window.MainWindow`).
- **Por qué:** menú, barra de herramientas y un banco de trabajo (datos + resultados + gráficas a la vez).
- **No usar:** QML/Qt Quick, `QDialog` como ventana principal, posicionamiento absoluto.

## Árbol de composición

```text
MainWindow
├── MenuBar + ToolBar (Ajustar, CSV, ejemplos)
├── StatusBar (n, SSE, ganador)
└── QSplitter horizontal
    ├── DataView (tabla x,y compacta)
    └── QSplitter vertical
        ├── QTabWidget: Lineal | Cuadrático | Comparación | Referencia
        └── ChartsView (Recta | Parábola | Ambos)
```

## Propiedad del estado

| Estado | Dueño | Lectores |
|--------|--------|----------|
| Pares (x, y) | `DatasetTableModel` + `AnalysisPresenter` | DataView, análisis |
| Resultado lineal / cuadrático | `AnalysisPresenter` (último `AnalysisReport`) | vistas de resultados y gráficas |
| Tema claro/oscuro | `ThemeManager` (aplicación) | MainWindow, estilos |
| Mensaje de error de validación | `AnalysisPresenter` → señal `analysis_failed` | StatusBar + DataView |

Flujo: acción de usuario → señal de vista → Presenter → `AnalysisService` (núcleo) → señal `analysis_ready` / `analysis_failed` → vistas se refrescan. Las vistas **no** se conectan entre sí.

## Modelo de hilos

Los ajustes con n académico (decenas o cientos de puntos) son O(n) y se ejecutan en el **hilo de UI**.

No hay `QThread` en la versión actual. Si en el futuro se importan CSV masivos, el worker se llamaría `AnalysisWorker` y emitiría `finished(AnalysisReport)` / `failed(str)` hacia el Presenter. Hasta entonces, YAGNI.

## Estados por superficie

| Superficie | Vacío | Inválido | Válido / éxito | Error |
|------------|-------|----------|----------------|-------|
| DataView | ilustración + CTA “Agregar fila” o cargar ejemplo | banner con mensaje (no numérico, longitudes, n insuficiente) | tabla editable | igual que inválido |
| LinearView / QuadraticView | “Ingrese datos y calcule” | oculto; el error vive en Datos | tarjetas y ecuación | mensaje breve |
| ComparisonView | vacío | — | tabla + modelo ganador + nota sobre sobreajuste | — |
| ChartsView | canvas vacío con leyenda | — | tres gráficas con ejes, título y leyenda | — |

No hay estado de red. “Busy” no aplica: el cálculo es inmediato.

## Señales semánticas

- `DataView.calculate_requested`
- `DataView.dataset_changed`
- `AnalysisPresenter.analysis_ready(report)`
- `AnalysisPresenter.analysis_failed(message)`
- `AnalysisPresenter.dataset_loaded(dataset)`

## Teclado y redimensionado

- Layouts (`QHBoxLayout` / `QVBoxLayout` / `QGridLayout`) desde el inicio; tamaño mínimo ~1100×700.
- Tab order: tabla → agregar/eliminar → calcular → navegación lateral.
