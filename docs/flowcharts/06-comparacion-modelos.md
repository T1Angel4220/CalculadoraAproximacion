# Comparación de modelos

Corresponde a `compare_models`, `narrate_comparison` y `ComparisonView`.

```mermaid
flowchart TD
    A[Métricas lineal y cuadrática] --> T["Escala = máximo de SST, SSE y 1<br/>tolerancia = max(1e-12, 1e-9 · escala)"]
    T --> B[Ordenar por SSE creciente]
    B --> C{¿Diferencia absoluta de SSE ≤ tolerancia?}
    C -->|Sí| D["Empate; recomendar la recta por simplicidad"]
    C -->|No| E[Ganador: menor SSE]
    D --> P{¿Ambos SSE ≤ tolerancia?}
    P -->|Sí| PERFECTO["Ajuste perfecto dentro de tolerancia<br/>reducción SSE: no aplica"]
    P -->|No| RED
    E --> RED["Reducción = 100 · (SSE lineal − SSE cuadrático) / SSE lineal<br/>no definida si SSE lineal ≤ tolerancia"]
    RED --> PEQ{¿Gana cuadrático con reducción mayor que 0 y menor que 5 %?}
    PEQ -->|Sí| AVISO[Conclusión: mejora pequeña del ajuste observado]
    PEQ -->|No| G[Conclusión según ganador o empate, SSE, R² y r lineal]
    AVISO --> VISTA
    PERFECTO --> VISTA
    G --> VISTA["ComparisonView: reducción SSE, R² y tabla SSE/SST/Syx/R²<br/>ecuaciones y conclusión"]
```

La tolerancia depende de los valores absolutos de ambos SST y SSE. `compare_models` conserva los valores originales y añade una nota sobre el anidamiento de modelos. El motor calcula R² ajustado, aunque la tabla actual no lo muestra. La conclusión describe ajuste sobre la muestra; una reducción de SSE no prueba por sí sola mejor predicción.
