# Cálculo de errores e indicadores

Corresponde a `compute_metrics` y `_signed_r`. `p` es el número de parámetros: 2 para la recta y 3 para la parábola.

```mermaid
flowchart TD
    A["y, ŷ, p, x opcional"] --> B["e = y − ŷ; SSE = Σ e²"]
    B --> C["ȳ = Σy/n; SST = Σ (y − ȳ)²"]
    C --> D{¿SST mayor que 1e-15?}
    D -->|No| E[R² no definido]
    D -->|Sí| F["R² = (SST − SSE) / SST"]
    C --> G{n > p?}
    G -->|No| H[Syx no definido]
    G -->|Sí| I["Syx = √(SSE / (n − p))"]
    C --> J{¿n mayor que p y 1; SST mayor que 1e-15?}
    J -->|Sí| K["R² ajustado = 1 − (SSE / (n − p)) / (SST / (n − 1))"]
    J -->|No| L[R² ajustado no definido]
    F --> M{¿Se proveyó x y R² está definido?}
    E --> M
    M -->|Sí| N["r = signo de Σ((x − x̄)(y − ȳ)) · √max(R², 0)"]
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

El signo de la covarianza se toma como positivo cuando es cero. Para la recta de mínimos cuadrados con intercepto, este cálculo de r coincide con Pearson. El servicio también invoca la función para el cuadrático; ese valor **no debe interpretarse como Pearson de x e y**. La comparación utiliza `linear_metrics.correlation` y la vista cuadrática solo interpreta R². Los grados de libertad n − p determinan cuándo Syx y R² ajustado están definidos.
