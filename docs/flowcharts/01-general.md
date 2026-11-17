# Diagrama de flujo general del sistema

Requisito 7 de la guía APE 04: desde el **inicio** hasta la **salida**, con menú principal, ingreso de datos, selección de opciones, ejecución de los métodos, presentación de resultados y finalización.

Código al que corresponde:

- `aproxlab.main:main`
- `MainWindow` (menú, toolbar, pestañas, Ajustar)
- `DataView` / `DatasetTableModel.numeric_pairs`
- `AnalysisPresenter.calculate`
- `AnalysisService.analyze`
- `LinearRegression.fit` · `QuadraticRegression.fit`
- `compute_metrics` · `compare_models`
- `ChartsView.show_report`
- `MainWindow.close` / Archivo → Salir

```mermaid
flowchart TD
    INICIO([Inicio]) --> MAIN["main(): QApplication + tema oscuro"]
    MAIN --> VENTANA["Crear MainWindow<br/>menú Archivo · Ejemplos · Ver · Ayuda"]
    VENTANA --> EJ_INICIAL["Cargar Datos de clase<br/>y calcular automáticamente"]
    EJ_INICIAL --> VALIDAR
    MENU{Menú principal<br/>¿qué elige el usuario?}

    MENU -->|Ingresar / editar pares x, y| DATOS["Ingreso de datos<br/>DataView: agregar, editar, eliminar filas"]
    DATOS --> MENU

    MENU -->|Limpiar| LIMPIAR["Vaciar tabla, resultados,<br/>comparación, gráficas y reporte"]
    LIMPIAR --> MENU

    MENU -->|Ejemplos| EJ["Cargar conjunto de ejemplo"]
    EJ --> VALIDAR

    MENU -->|Ajustar / F5| LEER["Leer tabla: ignorar filas vacías<br/>rechazar pares incompletos o no numéricos"]
    LEER -->|Pares válidos| VALIDAR
    LEER -->|Error| ERROR
    VALIDAR{"prepare_dataset<br/>vectores numéricos finitos<br/>igual longitud y al menos 2 x distintos"}

    VALIDAR -->|No| ERROR["Mostrar mensaje de error"]
    ERROR --> MENU

    VALIDAR -->|Sí| LINEAL["Ejecutar ajuste lineal<br/>LinearRegression.fit"]
    LINEAL -->|Éxito| CUAD["Ejecutar ajuste cuadrático<br/>QuadraticRegression.fit"]
    LINEAL -->|DatasetError| ERROR
    CUAD -->|DatasetError| ERROR
    CUAD -->|Éxito| MET["Calcular indicadores de ambos ajustes<br/>SSE, SST, Syx, R², R² ajustado y r"]
    MET --> COMP["Comparar modelos<br/>menor SSE"]
    COMP --> RES["Actualizar las vistas de resultados<br/>al terminar el arranque, mostrar la ventana"]

    RES --> R1["Pestaña Lineal:<br/>a0, a1, ecuación, SSE, SST, Syx, R², r"]
    RES --> R2["Pestaña Cuadrático:<br/>a0, a1, a2, ecuación, ŷ, residuos, SSE"]
    RES --> R3["Pestaña Comparación:<br/>ambos modelos y mejor ajuste"]
    RES --> R4["Gráficas:<br/>recta · parábola · ambos"]
    R1 --> MENU
    R2 --> MENU
    R3 --> MENU
    R4 --> MENU

    MENU -->|Seleccionar pestaña<br/>Lineal / Cuadrático / Comparación| VISTAS["Mostrar la vista elegida<br/>y sincronizar gráfica"]
    VISTAS --> MENU

    MENU -->|Pestaña Cuadrático:<br/>ocultar o mostrar la matriz| MATRIZ["Mostrar u ocultar ecuaciones,<br/>matriz aumentada y Gauss-Jordan"]
    MATRIZ --> MENU

    MENU -->|Ocultar / mostrar gráficas| VIS_GRAF["Cambiar visibilidad del panel<br/>conservar resultados y tamaños"]
    VIS_GRAF --> MENU

    MENU -->|Ampliar gráfica / Ver las tres| AMP["Ventana de gráficas a tamaño completo"]
    AMP --> MENU

    MENU -->|Exportar TXT o PNG| EXP["Guardar reporte o figura"]
    EXP --> MENU

    MENU -->|Ver: tema claro u oscuro| TEMA["apply_theme y redibujar gráficas"]
    TEMA --> MENU

    MENU -->|Archivo → Salir| FIN([Fin: cerrar aplicación])
```

## Lectura para la entrega

1. El programa arranca en `main`, crea la ventana y el **menú principal**, carga los **Datos de clase** y los analiza.
2. El usuario **ingresa datos**, carga un ejemplo o pulsa **Limpiar** para dejar la tabla y los resultados vacíos.
3. **Selecciona** Ajustar (u otra opción del menú).
4. Se **ejecutan** validación, lineal, cuadrático, métricas y comparación. El análisis conjunto requiere al menos tres puntos con tres valores distintos de x; cada estrategia valida sus requisitos.
5. Se **presentan** coeficientes, indicadores, conclusión y las tres gráficas.
6. El ciclo vuelve al menú hasta **Salir**.

Ocultar la matriz o las gráficas no ejecuta otra regresión. La exportación requiere un reporte previo; después de Limpiar se debe calcular de nuevo. Los errores se presentan en Datos y en la barra de estado, sin borrar automáticamente las vistas anteriores.
