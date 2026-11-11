# Planificación de asignaturas

Planificador: **`metric-ff -s 0`**. El dominio usa números (`:fluents`), que FF no entiende, y los problemas no tienen `:metric`, así que la configuración por defecto de Metric-FF no sirve (ver [README general](../README.md#metric-ff-y--s-0)).

## Qué contiene

Decidir en qué cuatrimestre se cursa cada asignatura respetando prerrequisitos,
correquisitos y límites de créditos (60 por cuatrimestre, 240 en total). Los créditos son
*fluents*. Los ficheros están en catalán.

- `assigs-metric-domain.pddl`: dominio con `:adl`, `:fluents` y `:equality`; la acción `assigna`
  tiene precondiciones con `exists`, `or` y comparaciones numéricas.
- `assigs-metric-prova-1/2/3.pddl`: el objetivo es cursar `A` en el cuatrimestre 3.
  - `prova-2` tiene solución.
  - `prova-1` (el cuatrimestre 3 ya tiene 55 créditos) y `prova-3` (ya hay 235 créditos en total)
    **no tienen solución a propósito**: Metric-FF demuestra que no existe ningún plan.

A pesar del nombre, los problemas no tienen `:metric`.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `assigs-metric-domain.pddl`

`assigs-metric-prova-1.pddl` — sin solución (el planificador demuestra que no hay plan):

```bash
metric-ff -s 0 -o assigs-metric-domain.pddl -f assigs-metric-prova-1.pddl
```

`assigs-metric-prova-2.pddl` — plan de 4 pasos:

```bash
metric-ff -s 0 -o assigs-metric-domain.pddl -f assigs-metric-prova-2.pddl
```

`assigs-metric-prova-3.pddl` — sin solución (el planificador demuestra que no hay plan):

```bash
metric-ff -s 0 -o assigs-metric-domain.pddl -f assigs-metric-prova-3.pddl
```

## Cambios respecto al original

Ninguno: los ficheros son los originales del curso.
