# ⚡ Calculadora Web de Corriente Eléctrica y Resistencia (DC)

Proyecto final de **Programación I** — Universidad de Margarita (UNIMAR), Decanato de Ingeniería y Afines.

## Propósito
Aplicación web hecha con **Python + Streamlit** que simula un circuito DC resistivo en serie
(fuente → cable de ida → carga → cable de retorno). A partir de tensión, resistencia de carga,
material, longitud de ida y sección del conductor calcula **Rc, Rt, I, Vc y Pc** con sus unidades.
Incluye historial persistente (JSON), sistema de Logs y exportación CSV.

> Simulación didáctica a 20 °C. No calcula ampacidad ni sirve para dimensionar instalaciones reales.

## Integrantes
| Integrante | Aporte principal |
|---|---|
| Bill | Líder Git, `config.py`, materiales, cálculos |
| Jamudi | Excepciones, validaciones (regex), script de pruebas mínimas |
| Omar | Decorador, generadores, sistema de Logs |
| Rafael | Historial JSON, reportes CSV, páginas Historial y Reportes |
| Elias | Interfaz principal (`app.py`), página Calculadora, Ayuda, README |
| Milcelys | Informe técnico, diagramas, pruebas funcionales y presentación |

## Requisitos
- Python 3.10 o superior
- Git

## Instalación (paso a paso)
```bash
git clone https://github.com/zzzbikezz/calculadora-unimar.git
cd calculadora-unimar

# Crear entorno virtual
python -m venv .venv

# Activarlo
#   Windows (PowerShell):  .venv\Scripts\Activate.ps1
#   Windows (cmd):         .venv\Scripts\activate.bat
#   Linux / macOS:         source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución
```bash
streamlit run app.py
```
Se abre en `http://localhost:8501`.

## Pruebas
```bash
python -m unittest discover -s tests -t .   # pruebas unitarias
python pruebas_minimas.py                   # las 6 pruebas del enunciado (deja evidencia en data/ y logs/)
```

## Funcionalidades
- **Calculadora**: 5 parámetros, calcular, limpiar, cargar ejemplo; resultados con unidades.
- **Validación**: acepta coma o punto; rechaza vacío, texto, 0, negativos, NaN e infinito; sección con regex (`2.5`, `2,5`, `2.5 mm2`, `2,5 mm²`).
- **Historial** (`data/historial.json`): guarda cada cálculo con id, fecha/hora, entradas y resultados; filtros por fecha y material; tolera JSON dañado.
- **Logs** (`logs/app.log`): módulo `logging`, niveles INFO/WARNING/ERROR, consulta en la interfaz.
- **Reportes**: exportación a CSV (carpeta `reportes/` o descarga) con encabezados y unidades.
- **Fundamentos/Ayuda**: parámetros, fórmulas, ejemplo, supuestos y limitaciones.

## Estructura
```
app.py                    Punto de entrada Streamlit (navegación)
config.py                 Rutas relativas y formato de logs
calculadora/              materiales.py · calculos.py · validaciones.py · excepciones.py
servicios/                historial.py · logs.py · reportes.py
utilidades/               decoradores.py · generadores.py
paginas/                  una página de interfaz por pestaña
data/historial.json       persistencia de cálculos
logs/app.log              eventos técnicos
reportes/                 CSV exportados
tests/                    pruebas unitarias
docs/                     guía del equipo y diagramas
```

## Contenidos de Programación I evidenciados
| Contenido | Dónde |
|---|---|
| Condicionales, ciclos, diccionarios, listas | `materiales.py`, `calculos.py`, `generadores.py` |
| Funciones y modularidad | todo el proyecto (interfaz / cálculos / servicios separados) |
| try/except y raise | `validaciones.py`, `historial.py`, `reportes.py` |
| Archivos JSON, CSV, .log con `with open` | `historial.py`, `reportes.py`, `logs.py` |
| Expresiones regulares (`re`) | `validaciones.py` (`PATRON_NUMERO`, `PATRON_SECCION`) |
| Generadores (`yield`) | `utilidades/generadores.py` |
| Decorador propio | `utilidades/decoradores.py` → `@registrar_operacion` |
| Git y GitHub | historial de commits del repositorio |
