# Ajuste lineal

Corresponde a `LinearRegression.fit` (sumatorias a mano, sin NumPy ni lstsq).

```mermaid
flowchart TD
    A[Entrada x, y] --> B[Validar n ≥ 2 y x no constante]
    B --> C[1. Sumatorias: Σx, Σy, Σx², Σxy]
    C --> D[2. Medias: x̄ = Σx/n, ȳ = Σy/n]
    D --> E[3. a1 = nΣxy − ΣxΣy sobre nΣx² − (Σx)²]
    E --> F[a0 = ȳ − a1 x̄]
    F --> G[4. Para cada i: ŷi = a0 + a1 xi, ei = yi − ŷi]
    G --> H[5. Sr = Σ e², St = Σ (yi − ȳ)²]
    H --> I[6. Sy/x = √ Sr / n−2]
    I --> J[7. r² = St − Sr sobre St]
    J --> K[8. r = signo(a1) √r²]
    K --> L[Interpretar r: fuerte / débil, positiva / negativa]
    L --> M[FitResult + LinearWorksheet]
```
