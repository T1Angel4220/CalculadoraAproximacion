# Ajuste lineal

Corresponde a `LinearRegression.fit` (sumatorias a mano, sin NumPy ni lstsq).

```mermaid
flowchart TD
    A[Entrada x, y] --> PREP[prepare_dataset: vectores finitos de igual longitud]
    PREP --> B{¿n ≥ 2 y al menos 2 x distintos?}
    PREP -->|Datos inválidos| Z
    B -->|No| Z[Error: no se ajusta la recta]
    B -->|Sí| C["1. Sumatorias: Σx, Σy, Σx², Σxy"]
    C --> D["2. Medias: x̄ = Σx/n, ȳ = Σy/n"]
    D --> E{"¿Valor absoluto del denominador menor que 1e-15?<br/>nΣx² − (Σx)²"}
    E -->|Sí| Z
    E -->|No| F["3. a1 = (nΣxy − ΣxΣy) / denominador"]
    F --> G["a0 = ȳ − a1 x̄"]
    G --> H["4. Para cada i: ŷi = a0 + a1 xi, ei = yi − ŷi"]
    H --> I["5. Sr = Σ e², St = Σ (yi − ȳ)²"]
    I --> J{¿n > 2?}
    J -->|No| K[Sy/x no está definido]
    J -->|Sí| L["6. Sy/x = √(Sr / (n − 2))"]
    K --> M{¿St mayor que 1e-15?}
    L --> M
    M -->|No| N["r² y r no están definidos"]
    M -->|Sí| O["7. r² = (St − Sr) / St"]
    O --> P["8. r = signo(a1) · √max(r², 0)"]
    P --> Q[Interpretar r]
    N --> R[FitResult + LinearWorksheet]
    Q --> R
```

Esta estrategia admite dos puntos; el análisis completo de la GUI también ejecuta la estrategia cuadrática y requiere al menos tres. `LinearWorksheet` contiene el desarrollo que muestra la vista; `AnalysisService` calcula además las métricas compartidas con `compute_metrics`.
