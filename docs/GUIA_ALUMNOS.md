# Guía para el alumnado: FF y Metric-FF en tu ordenador

Esta guía explica cómo instalar los planificadores **FF 2.3** y **Metric-FF 2.1** en Windows,
macOS o Linux, cómo probarlos con los ejemplos de la asignatura y qué hacer cuando algo no sale.
No hace falta compilar nada ni instalar Cygwin, MinGW o máquinas virtuales: solo Python.

## 1. Requisitos

- **Python 3.9 o posterior.** Compruébalo en una terminal (en Windows, *PowerShell*):

  ```bash
  python --version
  ```

  En macOS y Linux puede llamarse `python3`. Si no lo tienes:
  - Windows: instálalo desde <https://www.python.org/downloads/> y marca la casilla
    **"Add python.exe to PATH"** en la primera pantalla del instalador.
  - macOS: instálalo desde <https://www.python.org/downloads/> (o con Homebrew).
  - Linux: ya viene instalado; en Debian/Ubuntu instala también `python3-venv`
    (`sudo apt install python3-venv`).

- Sistemas con paquete preparado: Windows 10/11 de 64 bits (x64), macOS 11 o posterior (Intel y
  Apple Silicon) y Linux de 64 bits (x86-64 y ARM64).

## 2. Instalación

Lo recomendable es instalarlo en un **entorno virtual** (*venv*): una carpeta con su propio Python
donde se instala el paquete sin tocar el resto del sistema. Lo creas una vez y lo activas cada vez
que abras una terminal nueva.

### Windows (PowerShell)

```bash
py -m venv abia
```

```bash
abia\Scripts\Activate.ps1
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install fib-abia-planners
```

Si PowerShell no deja activar el entorno ("la ejecución de scripts está deshabilitada"), usa en su
lugar la consola clásica `cmd` y actívalo con `abia\Scripts\activate.bat`.

### macOS y Linux

```bash
python3 -m venv abia
```

```bash
source abia/bin/activate
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install fib-abia-planners
```

La primera orden actualiza `pip`: un `pip` antiguo no reconoce el paquete preparado para tu sistema e
intenta compilarlo, y falla. Con el entorno activado, el indicador de la terminal empieza por `(abia)`. Los comandos `ff`,
`metric-ff` y `fib-abia-planners` solo existen mientras el entorno está activado: en cada terminal
nueva, vuelve a ejecutar la orden de activación (desde la carpeta donde creaste `abia`).

### Comprobar la instalación

```bash
fib-abia-planners selftest
```

Prueba un problema de cada carpeta de ejemplos con `ff`, `metric-ff -s 0` y `metric-ff`, y debe
terminar con `TODO CORRECTO: 39 de 39 correctas.` (tarda unos segundos).

## 3. Primeros pasos con los ejemplos

Copia los ejemplos de la asignatura a una carpeta tuya:

```bash
fib-abia-planners examples mis-ejemplos
```

Entra en una de las carpetas y lanza el planificador indicando el dominio (`-o`) y el problema
(`-f`):

```bash
cd mis-ejemplos/hanoi
```

```bash
ff -o hanoi.pddl -f hanoi-3.pddl
```

La parte importante de la salida es el plan:

```
ff: found legal plan as follows

step    0: MOVE D1 D2 PEG3
        1: MOVE D2 D3 PEG2
        ...
        6: MOVE D1 PEG1 D2
```

Cada carpeta tiene un `README.md` con lo que contiene y un comando listo para copiar por cada
problema, y `mis-ejemplos/README.md` resume todos los dominios y qué planificador usar en cada uno.

## 4. Tus propios dominios y problemas

Escribe el dominio y el problema en dos ficheros de texto (`.pddl`) en la misma carpeta, entra en
ella y ejecuta:

```bash
ff -o mi-dominio.pddl -f mi-problema.pddl
```

También puedes indicar la carpeta con `-p` (debe terminar en `/`):

```bash
ff -p ruta/a/mi-carpeta/ -o mi-dominio.pddl -f mi-problema.pddl
```

Para guardar la salida en un fichero:

```bash
ff -o mi-dominio.pddl -f mi-problema.pddl > salida.txt
```

## 5. ¿FF o Metric-FF?

| Tu dominio | Comando |
|---|---|
| Sin números (sin `:fluents` ni `:metric`) | `ff -o D -f P` |
| Con números (`:fluents`), sin `(:metric ...)` en el problema | `metric-ff -s 0 -o D -f P` |
| Con `(:metric minimize ...)` en el problema | `metric-ff -o D -f P` |

`metric-ff`, sin `-s`, busca el plan **más barato** según la métrica del problema; si el problema
no tiene `:metric`, se para con `Optimization criterion not established` y el comando te sugiere
usar `-s 0`. Más detalles en `mis-ejemplos/README.md`.

Para ver todas las opciones de cada planificador, ejecútalo sin argumentos (`ff` o `metric-ff`).
Las más útiles:

| Opción | Planificador | Para qué |
|---|---|---|
| `-s N` | `metric-ff` | Estrategia de búsqueda (`0` a `5`; por defecto `5`) |
| `-w N` | `metric-ff` | Peso de A\* con `-s 3`, `4` y `5` (por defecto `5`) |
| `-i 101` | ambos | Muestra el dominio y el problema tal como los ha leído (útil para buscar errores) |

## 6. Cómo leer la salida

| Mensaje | Qué significa |
|---|---|
| `found legal plan as follows` | Ha encontrado un plan; los pasos van a continuación. |
| `goal can be simplified to FALSE` | El objetivo es imposible: no hay solución. |
| `problem proven unsolvable` | Ha explorado todo y no hay solución. |
| `goal can be simplified to TRUE` | El estado inicial ya cumple el objetivo: el plan está vacío. |
| `syntax error in line N` | Error en el fichero PDDL, en la línea N o poco antes. |
| `Enforced Hill-climbing failed !` | No es un error: la primera estrategia se ha atascado y prueba otra. |

El plan encontrado **no tiene por qué ser el más corto** (salvo con `metric-ff` y `:metric`,
que intenta minimizar el coste). En otro sistema operativo el plan puede variar un poco: cualquier
plan que el planificador da como válido es una solución correcta.

## 7. Problemas frecuentes

**"ff no se reconoce como un comando" / "command not found".** El entorno virtual no está
activado en esta terminal: actívalo (apartado 2) y vuelve a probar.

**`error: externally-managed-environment` al hacer `pip install`.** Estás instalando fuera de
un entorno virtual en un sistema que no lo permite (Ubuntu, Debian, Homebrew…). Crea y activa el
entorno del apartado 2.

**`can't find operator file` o `can't find fact file`.** No encuentra el fichero: comprueba el
nombre y que estás en la carpeta correcta (`ls` en macOS/Linux, `dir` en Windows).

**`syntax error in line 2, ':FLUENTS'` con `ff`.** FF no admite números: usa `metric-ff`.

**`Error! Optimization criterion not established.`** El problema no tiene `:metric` y estás usando
`metric-ff` sin `-s`: usa `metric-ff -s 0`.

**El planificador no termina.** Para con **Ctrl+C**. Algunos problemas son demasiado difíciles
para la estrategia elegida (en `mis-ejemplos/blocks/` hay un ejemplo). Prueba otra estrategia de
Metric-FF (`-s 0`, `-s 3`…), revisa si el dominio permite acciones inútiles o en bucle, o
prueba con un problema más pequeño.

**Errores extraños con nombres.** En PDDL los nombres (dominio, problema, objetos, acciones…)
deben empezar por una letra: Metric-FF falla, por ejemplo, con `(problem 7personas)`.

## 8. Actualizar y desinstalar

Con el entorno activado:

```bash
pip install --upgrade fib-abia-planners
```

```bash
pip uninstall fib-abia-planners
```

Para borrarlo todo, basta con borrar la carpeta `abia` del entorno virtual (tus ejemplos y
ficheros `.pddl` están en otras carpetas y no se tocan).

## 9. Si algo falla

Ejecuta:

```bash
fib-abia-planners selftest --all
```

```bash
fib-abia-planners info
```

y envía al profesorado la salida completa de los dos comandos, junto con los ficheros `.pddl`
y el comando que estabas usando.
