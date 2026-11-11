# Logistics

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

El dominio Logistics de la competición internacional de planificación (IPC): transportar paquetes
entre ciudades con camiones (dentro de una ciudad) y aviones (entre aeropuertos).

- `logistics.pddl`: dominio STRIPS **sin `:typing`**: los tipos de objeto se expresan con
  predicados unarios estáticos (`truck`, `airplane`, `city`…) que el problema declara en `:init`.
- `log-3-2.pddl`: 3 ciudades (cada una con un camión, una oficina y un aeropuerto), un avión y
  2 paquetes. Este fichero tiene finales de línea de Windows (CRLF): los planificadores lo leen igual.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `logistics.pddl`

`log-3-2.pddl` — plan de 18 pasos:

```bash
ff -o logistics.pddl -f log-3-2.pddl
```

## Cambios respecto al original

Ninguno: los ficheros son los originales del curso.
