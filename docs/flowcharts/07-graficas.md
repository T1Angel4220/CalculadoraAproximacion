# Generación de gráficas

Corresponde a `dense_curve`, `plot_scatter_and_fits`, `ChartsView` y los controles de gráficas de `MainWindow`. Se usan los coeficientes del reporte, sin volver a ajustar los modelos.

```mermaid
flowchart TD
    A[AnalysisReport + paleta del tema] --> B[Evaluar polinomios en malla densa de 200 puntos]
    B --> C[Gráfica 1: puntos + recta]
    B --> D[Gráfica 2: puntos + parábola]
    B --> E[Gráfica 3: puntos + ambos]
    C --> F[Título, ejes, leyenda, grid]
    D --> F
    E --> F
    F --> ACCION{Acción de usuario}
    ACCION -->|Cambiar pestaña de resultados| TAB[Sincronizar Recta, Parábola o Ambos]
    ACCION -->|Ocultar / mostrar gráficas| VIS[Conservar reporte y tamaños del splitter]
    ACCION -->|Ampliar gráfica| AMP[Diálogo con gráfica actual]
    ACCION -->|Ver las tres| TODAS[Diálogo con tres pestañas]
    ACCION -->|Cambiar tema| TEMA[Actualizar paleta y redibujar con el mismo reporte]
    ACCION -->|Limpiar| VACIO["Borrar reporte, puntos, curvas y leyendas<br/>también en los paneles ocultos"]
    ACCION -->|Exportar PNG| G{¿Hay reporte?}
    G -->|No| ERR[Mostrar error: calcule un ajuste]
    G -->|Sí| DESTINO{Destino elegido}
    DESTINO -->|Actual| H[save_current_png]
    DESTINO -->|Las tres| I[save_all_png]
```

Los diálogos ampliados son modales y se abren solo con un reporte. Al cambiar la pestaña Lineal/Cuadrático/Comparación se selecciona Recta/Parábola/Ambos; el usuario también puede cambiar la pestaña de la gráfica por separado. Exportar o cambiar el tema no recalcula regresiones.
