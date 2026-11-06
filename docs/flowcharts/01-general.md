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
    MAIN --> VENTANA["Mostrar MainWindow<br/>menú Archivo · Ejemplos · Ver · Ayuda"]
    VENTANA --> MENU{Menú principal<br/>¿qué elige el usuario?}

    MENU -->|Ingresar / editar pares x, y| DATOS["Ingreso de datos<br/>DataView: agregar, editar, eliminar filas"]
    DATOS --> MENU

    MENU -->|Ejemplos| EJ["Cargar conjunto de ejemplo"]
    EJ --> VALIDAR

    MENU -->|Ajustar / F5| VALIDAR{"Validar datos<br/>misma cantidad x e y<br/>numéricos y finitos<br/>n suficiente"}

    VALIDAR -->|No| ERROR["Mostrar mensaje de error"]
    ERROR --> MENU

    VALIDAR -->|Sí| LINEAL["Ejecutar ajuste lineal<br/>LinearRegression.fit"]
    LINEAL --> CUAD["Ejecutar ajuste cuadrático<br/>QuadraticRegression.fit"]
    CUAD --> MET["Calcular indicadores<br/>SSE, SST, Syx, R², r"]
    MET --> COMP["Comparar modelos<br/>menor SSE"]
    COMP --> RES["Presentar resultados"]

    RES --> R1["Pestaña Lineal:<br/>a0, a1, ecuación, SSE, SST, Syx, R², r"]
    RES --> R2["Pestaña Cuadrático:<br/>a0, a1, a2, ecuación, ŷ, residuos, SSE"]
    RES --> R3["Pestaña Comparación:<br/>ambos modelos y mejor ajuste"]
    RES --> R4["Gráficas:<br/>recta · parábola · ambos"]
    R1 --> MENU
    R2 --> MENU
    R3 --> MENU
    R4 --> MENU

    MENU -->|Seleccionar pestaña<br/>Lineal / Cuadrático / Comparación / Referencia| VISTAS["Mostrar la vista elegida<br/>y sincronizar gráfica"]
    VISTAS --> MENU

    MENU -->|Ampliar gráfica / Ver las tres| AMP["Ventana de gráficas a tamaño completo"]
    AMP --> MENU

    MENU -->|Exportar TXT o PNG| EXP["Guardar reporte o figura"]
    EXP --> MENU

    MENU -->|Ver: tema claro u oscuro| TEMA["apply_theme y redibujar gráficas"]
    TEMA --> MENU

    MENU -->|Archivo → Salir| FIN([Fin: cerrar aplicación])
```

## Lectura para la entrega

1. El programa arranca en `main`, crea la ventana y el **menú principal**.
2. El usuario **ingresa datos** o carga un ejemplo.
3. **Selecciona** Ajustar (u otra opción del menú).
4. Se **ejecutan** validación, lineal, cuadrático, métricas y comparación.
5. Se **presentan** coeficientes, indicadores, conclusión y las tres gráficas.
6. El ciclo vuelve al menú hasta **Salir**.
