# Ajuste lineal

Corresponde a `LinearRegression.fit`.

```mermaid
flowchart TD
    A[Entrada x, y] --> B[prepare_dataset]
    B --> C[require_min_points n ≥ 2]
    C --> D{¿Al menos 2 x distintos?}
    D -->|No| E[DegenerateDesignError]
    D -->|Sí| F[Matriz de diseño 1 | x]
    F --> G[np.linalg.lstsq]
    G --> H[ŷ = X a]
    H --> I[residuos = y - ŷ]
    I --> J[Ecuación format_polynomial]
    J --> K[FitResult lineal]
```
