# Ajuste polinomial de segundo grado

Corresponde a `QuadraticRegression.fit`.

```mermaid
flowchart TD
    A[Entrada x, y] --> B[prepare_dataset]
    B --> C[require_min_points n ≥ 3]
    C --> D{¿Al menos 3 x distintos?}
    D -->|No| E[DegenerateDesignError]
    D -->|Sí| F[Matriz de diseño 1 | x | x²]
    F --> G{rango X = 3?}
    G -->|No| E
    G -->|Sí| H[np.linalg.lstsq]
    H --> I[ŷ y residuos]
    I --> J[Coeficientes a0, a1, a2]
    J --> K[FitResult cuadrático]
```
