# Ajuste polinomial de segundo grado

Corresponde a `QuadraticRegression.fit`. El sistema se arma y se resuelve a mano.

En la pestaña Cuadrático, el botón **Ocultar / Mostrar cálculo de la matriz** solo esconde o vuelve a mostrar las ecuaciones normales, la matriz aumentada y el Gauss-Jordan. El ajuste se calcula igual en los dos casos. El botón se deshabilita cuando no hay un resultado y conserva la preferencia de visibilidad después de Limpiar.

```mermaid
flowchart TD
    A[Entrada x, y] --> B[prepare_dataset]
    B -->|Datos inválidos| ERR[DatasetError]
    B --> C[require_min_points n ≥ 3]
    C -->|No alcanza n| ERR
    C --> D{¿Al menos 3 x distintos?}
    D -->|No| E[DegenerateDesignError]
    D -->|Sí| F["Sumatorias Σx, Σx², Σx³, Σx⁴, Σy, Σxy, Σx²y"]
    F --> G[Ecuaciones normales 3×3]
    G --> H[Matriz aumentada]
    H --> I[Gauss-Jordan: siguiente columna]
    I --> J{¿Valor absoluto del pivote ≥ 1e-12?}
    J -->|No| BUSCAR{¿Hay una fila inferior con pivote válido?}
    BUSCAR -->|No| E
    BUSCAR -->|Sí| CAMBIO[Intercambiar filas y registrar la operación]
    CAMBIO --> NORMALIZAR
    J -->|Sí| NORMALIZAR[Normalizar pivote y eliminar debajo; registrar matrices]
    NORMALIZAR --> MAS{¿Más columnas?}
    MAS -->|Sí| I
    MAS -->|No| ARRIBA[Eliminar encima de los pivotes en orden inverso]
    ARRIBA --> K["Extraer a0, a1, a2 y pasos registrados"]
    K --> L["ŷ, e, e², Sr y St"]
    L --> M{¿n > 3?}
    M -->|No| N[Sy/x no está definido]
    M -->|Sí| O["Sy/x = √(Sr / (n − 3))"]
    N --> P{¿St mayor que 1e-15?}
    O --> P
    P -->|No| Q[r² no está definido]
    P -->|Sí| R["r² = (St − Sr) / St"]
    Q --> S[FitResult + QuadraticWorksheet]
    R --> S
```

`gauss_jordan_steps` lanza `ZeroDivisionError` si no encuentra pivote válido; la estrategia lo convierte en `DegenerateDesignError`. El desarrollo incluye sumatorias, matriz inicial, operaciones y errores. Ocultar la matriz conserva esos resultados y permite volver a mostrarlos sin llamar al núcleo.
