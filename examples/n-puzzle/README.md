# 8-puzzle (puzzle deslizante)

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

El puzzle de 8 piezas en un tablero de 3×3: deslizar las piezas al hueco hasta llegar a la
configuración objetivo.

- `slidetile.pddl`: dominio STRIPS con cuatro acciones (`move-up`, `move-down`, `move-left`,
  `move-right`). Cada posición se representa con una coordenada horizontal y otra vertical.
- `eight01.pddl`: una de las dos instancias más difíciles del 8-puzzle; la solución óptima tiene
  31 movimientos (Reinefeld). FF no busca el plan óptimo: encuentra planes válidos pero más largos.
  Fíjate en que algunas acciones del plan repiten argumentos (p. ej. `MOVE-RIGHT T1 P2 P1 P1`):
  es correcto, una misma coordenada puede aparecer dos veces.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `slidetile.pddl`

`eight01.pddl` — plan de 63 pasos:

```bash
ff -o slidetile.pddl -f eight01.pddl
```

## Cambios respecto al original

Ninguno: los ficheros son los originales del curso.
