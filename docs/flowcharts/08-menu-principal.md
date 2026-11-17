# Menú principal

Corresponde a `MainWindow._build_menus`, la barra de ejemplos y las pestañas del banco de trabajo.

```mermaid
flowchart TD
    A[Menú principal] --> B{Opción}
    B -->|Ingreso: tabla x, y| C[DataView]
    B -->|Limpiar: Datos, toolbar o Archivo| C2["Vaciar datos, resultados y reporte<br/>reiniciar selector; n = 0"]
    B -->|Ajustar F5| D[Validar y AnalysisPresenter.calculate]
    B -->|Pestaña Lineal| E[LinearView]
    B -->|Pestaña Cuadrático| F[QuadraticView]
    B -->|Cuadrático: ocultar o mostrar matriz| F2["Ecuaciones, matriz aumentada y Gauss-Jordan<br/>habilitado solo con resultado; sin recalcular"]
    B -->|Pestaña Comparación| G[ComparisonView]
    B -->|Gráficas: Recta / Parábola / Ambos| I[ChartsView]
    B -->|Ampliar / Ver las tres| J[Diálogo de gráficas]
    B -->|Toolbar o Ver: ocultar / mostrar gráficas| V[Conservar resultados y cambiar visibilidad]
    B -->|Ejemplos| K[load_example y calcular]
    B -->|Exportar TXT o PNG| L[QFileDialog]
    B -->|Ver: tema| M[apply_theme]
    B -->|Ayuda| N[Acerca de]
    B -->|Archivo → Salir| O[Cerrar · Fin]
    C --> A
    C2 --> A
    D --> A
    F2 --> A
    E --> A
    F --> A
    G --> A
    I --> A
    J --> A
    V --> A
    K --> A
    L --> A
    M --> A
    N --> A
```

Al iniciar se carga **Datos de clase** y se calcula el primer reporte. Las opciones del diagrama abarcan menús, toolbar, controles de Datos y pestañas. Archivo contiene exportación TXT, PNG actual, las tres PNG, Limpiar y Salir; Ver contiene temas y visibilidad de gráficas. No hay una opción de importación CSV en el menú actual.
