# Viajante de comercio (TSP)

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

El problema del viajante de comercio en versión STRIPS: visitar todas las ciudades una vez y
volver a la ciudad de salida.

- `tsp.pddl`: dominio. `go-along`/`go-against` recorren una arista en un sentido u otro;
  `return-along`/`return-against` cierran el recorrido volviendo a la ciudad de salida.
- `tsp-10.pddl`: 10 ciudades.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `tsp.pddl`

`tsp-10.pddl` — plan de 10 pasos:

```bash
ff -o tsp.pddl -f tsp-10.pddl
```

## Cambios respecto al original

- `return-against` exigía que la ciudad de llegada estuviera **sin visitar** (`(not-visited ?y)`)
  en lugar de ser la ciudad de **salida** (`(starting ?y)`), como en `return-along`. Con ese error
  la acción nunca podía formar parte de un plan válido. Corregido.
