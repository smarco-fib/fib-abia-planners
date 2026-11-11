# Transporte aéreo de carga

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

Aviones que transportan cargas entre aeropuertos: cargar, volar y descargar. El mismo dominio
modelado de dos maneras:

- `C5-aircargo-domain3ops.pddl`: STRIPS **sin tipos**. Qué es avión, carga o aeropuerto lo dicen
  predicados unarios (`Avion`, `Carga`, `Aeropuerto`) que aparecen en las precondiciones.
  Problemas: `C5-aircargo-problem1` … `problem4`.
- `C5-aircargo-domain3ops-typed.pddl`: la misma idea **con `:typing`**: los tipos sustituyen a esos
  predicados y las acciones quedan más cortas. Problemas: `C5-aircargo-problem1-typed`,
  `problem3-typed`.

Comparar `problem1` con `problem1-typed` (o `problem3` con `problem3-typed`) muestra el mismo
problema en las dos modelizaciones.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `C5-aircargo-domain3ops.pddl`

`C5-aircargo-problem1.pddl` — plan de 6 pasos:

```bash
ff -o C5-aircargo-domain3ops.pddl -f C5-aircargo-problem1.pddl
```

`C5-aircargo-problem2.pddl` — plan de 6 pasos:

```bash
ff -o C5-aircargo-domain3ops.pddl -f C5-aircargo-problem2.pddl
```

`C5-aircargo-problem3.pddl` — plan de 31 pasos:

```bash
ff -o C5-aircargo-domain3ops.pddl -f C5-aircargo-problem3.pddl
```

`C5-aircargo-problem4.pddl` — plan de 27 pasos:

```bash
ff -o C5-aircargo-domain3ops.pddl -f C5-aircargo-problem4.pddl
```


#### Dominio `C5-aircargo-domain3ops-typed.pddl`

`C5-aircargo-problem1-typed.pddl` — plan de 6 pasos:

```bash
ff -o C5-aircargo-domain3ops-typed.pddl -f C5-aircargo-problem1-typed.pddl
```

`C5-aircargo-problem3-typed.pddl` — plan de 30 pasos:

```bash
ff -o C5-aircargo-domain3ops-typed.pddl -f C5-aircargo-problem3-typed.pddl
```

## Cambios respecto al original

- Dominio sin tipos, acción `descarga`: borraba `(En ?c ?av)` (que nunca es cierto) en lugar de
  `(Dentro ?c ?av)`, de modo que la carga descargada seguía también dentro del avión. Corregido
  (la versión con tipos ya era correcta).
