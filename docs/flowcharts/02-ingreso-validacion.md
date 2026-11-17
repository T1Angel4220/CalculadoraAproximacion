# Ingreso y validación de datos

Corresponde a `DatasetTableModel.numeric_pairs`, `prepare_dataset` y las validaciones de cada estrategia (`require_min_points` y valores distintos de x). La tabla admite punto o coma como separador decimal.

```mermaid
flowchart TD
    L0[Limpiar] --> L1["Cinco filas vacías, sin resultados ni reporte<br/>n = 0; selector de ejemplos reiniciado"]
    A[Leer siguiente fila de la tabla] --> B{¿x e y vacíos?}
    B -->|Sí| C[Ignorar fila]
    B -->|No| D{¿Están ambos valores?}
    D -->|No| ERR[NonNumericDataError: fila incompleta o valor no numérico]
    D -->|Sí| E{¿Convertir ambos a float?}
    E -->|No| ERR
    E -->|Sí| G[Acumular en vectores x, y]
    C --> H{¿Más filas?}
    G --> H
    H -->|Sí| A
    H -->|No| I{¿Hay al menos un par?}
    I -->|No| J[InsufficientDataError]
    I -->|Sí| PREP["prepare_dataset en AnalysisService<br/>convertir x e y a vectores numéricos"]
    PREP --> FINITOS{¿Unidimensionales y finitos?}
    FINITOS -->|No| ERR
    FINITOS -->|Sí| K{¿Misma longitud?}
    K -->|No| L[LengthMismatchError]
    K -->|Sí| DIST{¿Al menos 2 x distintos?}
    DIST -->|No| DEG[DegenerateDesignError]
    DIST -->|Sí| M[Vectores listos para las estrategias]
    M --> LIN["Lineal: n ≥ 2 y al menos 2 x distintos"]
    LIN --> CUAD["Cuadrático: n ≥ 3 y al menos 3 x distintos"]
    LIN -->|n insuficiente| J
    CUAD -->|n insuficiente| J
    LIN -->|x degenerados| DEG
    CUAD -->|x degenerados| DEG
    CUAD -->|Validación correcta| OK[Continuar ajuste y comparación]
```

Los ejemplos y CSV cargados mediante el Presenter entregan vectores al servicio; no pasan por la lectura de filas de `numeric_pairs`. La GUI actual carga ejemplos, pero no expone un botón de importación CSV. El análisis conjunto solo produce un reporte cuando los dos ajustes terminan correctamente.
