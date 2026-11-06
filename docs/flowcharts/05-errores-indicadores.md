# Cálculo de errores e indicadores

Corresponde a `compute_metrics`.

```mermaid
flowchart TD
    A[y, ŷ, p, x opcional] --> B[SSE = Σ (y - ŷ)²]
    B --> C[SST = Σ (y - ȳ)²]
    C --> D{SST > 0?}
    D -->|No| E[R² no definido]
    D -->|Sí| F[R² = 1 - SSE/SST]
    C --> G{n > p?}
    G -->|No| H[Syx no definido]
    G -->|Sí| I[Syx = √ SSE / n-p]
    C --> J{n > p y SST > 0?}
    J -->|Sí| K[R² ajustado]
    J -->|No| L[R² ajustado no definido]
    A --> M{¿Se proveyó x y hay varianza?}
    M -->|Sí| N[r = Pearson x, y]
    M -->|No| O[r no definido]
    F --> P[FitMetrics]
    E --> P
    I --> P
    H --> P
    K --> P
    L --> P
    N --> P
    O --> P
```
