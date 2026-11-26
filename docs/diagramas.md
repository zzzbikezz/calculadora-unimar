# Diagramas para el informe (formato Mermaid)

Cómo usarlos: abrir https://mermaid.live → pegar el código de un diagrama → **Actions → PNG** → insertar en el
informe con su título y una explicación breve. Todos corresponden al código real del proyecto.

## 1. Casos de uso general
```mermaid
flowchart LR
    U([Usuario])
    U --> C1(Calcular corriente y resistencia)
    U --> C2(Limpiar formulario / cargar ejemplo)
    U --> C3(Consultar y filtrar historial)
    U --> C4(Consultar logs)
    U --> C5(Exportar CSV)
    U --> C6(Leer ayuda y fundamentos)
    C1 -.incluye.-> V(Validar datos)
    C1 -.incluye.-> H(Guardar en historial)
    C1 -.incluye.-> L(Registrar eventos en logs)
```

## 2. Flujo general de la aplicación
```mermaid
flowchart TD
    A([streamlit run app.py]) --> B[configurar_logger e inicializar_historial]
    B --> C[Log INFO: aplicación iniciada]
    C --> D{Pestaña elegida}
    D --> E[Calculadora]
    D --> F[Historial]
    D --> G[Logs]
    D --> H[Ayuda]
    D --> I[Reportes]
```

## 3. Arquitectura / módulos
```mermaid
flowchart TD
    APP[app.py] --> PAG[paginas/*]
    PAG --> CAL[calculadora/: validaciones, calculos, materiales, excepciones]
    PAG --> SER[servicios/: historial, logs, reportes]
    CAL --> UTI[utilidades/: decoradores]
    SER --> UTI
    SER --> GEN[utilidades/generadores]
    SER --> CFG[config.py]
    SER --> F1[(data/historial.json)]
    SER --> F2[(logs/app.log)]
    SER --> F3[(reportes/*.csv)]
```

## 4. Flujo de la calculadora
```mermaid
flowchart TD
    A[Usuario escribe 5 datos] --> B[Clic en Calcular]
    B --> C{validar_entradas}
    C -- inválido --> D[Mensaje de error + Log WARNING]
    C -- válido --> E[mm² a m²]
    E --> F[Ltotal = 2L]
    F --> G[Rc = ρ·Ltotal/A]
    G --> H[Rt = Rcarga + Rc]
    H --> I[I = V/Rt]
    I --> J[Vc = I·Rc y Pc = I²·Rc]
    J --> K[guardar_calculo en JSON]
    K --> L[Mostrar resultados con unidades + Log INFO]
```

## 5. Flujo del historial
```mermaid
flowchart TD
    A[Abrir Historial] --> B{¿Existe historial.json?}
    B -- No --> C[Crear archivo vacío + Log WARNING/INFO]
    B -- Sí --> D{¿JSON legible?}
    C --> D
    D -- Dañado --> E[Respaldar archivo, reiniciar vacío + Log ERROR]
    D -- Correcto --> F[Cargar lista de registros + Log INFO]
    E --> F
    F --> G[Filtrar por material / fecha con generador]
    G --> H{¿Hay coincidencias?}
    H -- No --> I[Aviso + Log WARNING]
    H -- Sí --> J[Mostrar tabla]
```

## 6. Flujo de Logs
```mermaid
flowchart TD
    A[Evento en el programa] --> B{Tipo}
    B -- Operación normal --> C[INFO]
    B -- Dato inválido / archivo inexistente / filtro vacío --> D[WARNING]
    B -- Fallo de lectura, escritura o JSON corrupto --> E[ERROR]
    C --> F[(logs/app.log)]
    D --> F
    E --> F
    F --> G[Pestaña Logs: generador lee y filtra líneas recientes]
```

## 7. Flujo de reportes
```mermaid
flowchart TD
    A[Abrir Reportes] --> B[Cargar historial]
    B --> C[Elegir cálculos o todos]
    C --> D{¿Hay registros?}
    D -- No --> E[Aviso + Log WARNING]
    D -- Sí --> F[Convertir a filas con unidades]
    F --> G[Escribir CSV en reportes/ o descargar]
    G --> H[Log INFO: exportación correcta]
```
