# Ejemplos de planificación (ABIA)

Ejemplos de dominios y problemas en PDDL para practicar con los planificadores **FF 2.3** y
**Metric-FF 2.1**. Cada carpeta tiene su propio `README.md` con lo que contiene y un comando listo
para copiar por cada problema.

## Cómo ejecutar un ejemplo

Copia los ejemplos a una carpeta tuya y entra en la del dominio que quieras:

```bash
abia-planners examples mis-ejemplos
```

```bash
cd mis-ejemplos/hanoi
```

Y lanza el planificador indicando el dominio (`-o`) y el problema (`-f`):

```bash
ff -o hanoi.pddl -f hanoi-3.pddl
```

## Qué planificador usar

| Carpeta | Contenido | Planificador |
|---|---|---|
| [`hanoi/`](hanoi/) | Torres de Hanoi, de 3 a 8 discos | `ff` |
| [`n-puzzle/`](n-puzzle/) | 8-puzzle (puzzle deslizante) | `ff` |
| [`tsp/`](tsp/) | Viajante de comercio | `ff` |
| [`logistics/`](logistics/) | Logistics (IPC): paquetes, camiones y aviones | `ff` |
| [`ascensor/`](ascensor/) | Miconic (IPC): un ascensor y sus pasajeros | `ff` |
| [`rovers/`](rovers/) | Rovers (IPC): robots exploradores en Marte | `ff` |
| [`aircargo/`](aircargo/) | Transporte aéreo de carga, sin tipos y con tipos | `ff` |
| [`blocks/`](blocks/) | Mundo de bloques con 2, 4 y 6 operadores, y un ejercicio STRIPS → PDDL | `ff` |
| [`vector/`](vector/) | Ordenar un vector, cuatro modelizaciones | `ff` |
| [`sharebath/`](sharebath/) | Baño compartido por siete personas | `ff` |
| [`smartbus/`](smartbus/) | Autobús con pasajeros normales y de movilidad reducida; cinco variantes | `ff` o `metric-ff -s 0` |
| [`asignaturas/`](asignaturas/) | Asignar asignaturas a cuatrimestres con créditos (*fluents*) | `metric-ff -s 0` |
| [`binpacking/`](binpacking/) | Empaquetado minimizando contenedores (`:metric`) | `metric-ff` |

La regla es sencilla:

- **Sin números** (sin `:fluents` ni `:metric`): `ff`.
- **Con números pero sin `:metric`**: `metric-ff -s 0`.
- **Con `:metric`** (hay algo que minimizar): `metric-ff`.

## Metric-FF y `-s 0`

Metric-FF tiene varias estrategias de búsqueda, que se eligen con `-s`:

| `-s` | Estrategia | ¿Minimiza la métrica? |
|---|---|---|
| `0` | El FF clásico: *Enforced Hill-Climbing* y, si se atasca, búsqueda *best-first* | No |
| `1`, `2` | Solo búsqueda *best-first* | No |
| `3` | A* ponderado | Sí |
| `4` | A\*-epsilon | Sí |
| `5` (**por defecto**) | *Enforced Hill-Climbing* y, si se atasca, A\*-epsilon | Sí |

Las estrategias 4 y 5 buscan el plan **más barato** según la línea `(:metric minimize ...)` del
problema. Si el problema no tiene `:metric` (o la métrica no se puede usar, por ejemplo con
`maximize`), Metric-FF se detiene antes de empezar con este mensaje:

```
Error! Optimization criterion not established.
A*epsilon not defined.
```

No es un fallo de tu dominio: significa que no hay nada que minimizar. Usa **`-s 0`**, que busca
un plan válido sin optimizar ningún coste:

```bash
metric-ff -s 0 -o dominio.pddl -f problema.pddl
```

## Cómo leer la salida

- `ff: found legal plan as follows` y a continuación `step 0: ...`, `1: ...`: el plan encontrado.
- `ff: goal can be simplified to FALSE` o `problem proven unsolvable`: el problema **no tiene
  solución**, y el planificador lo ha demostrado.
- `syntax error in line N`: error de sintaxis en el fichero (FF da este error si el dominio usa
  `:fluents`; para eso está Metric-FF).
- Al final, `time spent:` resume el tiempo de cada fase.

Los planificadores no buscan el plan más corto (salvo Metric-FF con `:metric`, que intenta
reducir el coste). En sistemas distintos (Windows, macOS, Linux) el plan encontrado puede variar
ligeramente; cualquier plan que el planificador dé por válido es una solución correcta.

## Procedencia

Los ejemplos vienen del material del curso ABIA (UPC). Varios proceden de la competición
internacional de planificación (Logistics, Miconic, Rovers) y las Torres de Hanoi son una
formalización de Héctor Geffner. Algunos ficheros se han corregido o comentado; cada `README.md`
indica los cambios respecto al original.
