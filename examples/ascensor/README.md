# Ascensor (Miconic)

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

El dominio Miconic (IPC-2000): un ascensor debe recoger a cada pasajero en su planta de origen y
dejarlo en su planta de destino.

- `miconic.pddl`: dominio ADL con tipos (`passenger`, `floor`) y tres acciones: `up`, `down` y
  `stop` (al parar, suben y bajan los pasajeros que corresponde, con efectos condicionales).
- `miconic01.pddl` … `miconic05.pddl`: problemas de tamaño creciente.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `miconic.pddl`

`miconic01.pddl` — plan de 11 pasos:

```bash
ff -o miconic.pddl -f miconic01.pddl
```

`miconic02.pddl` — plan de 16 pasos:

```bash
ff -o miconic.pddl -f miconic02.pddl
```

`miconic03.pddl` — plan de 21 pasos:

```bash
ff -o miconic.pddl -f miconic03.pddl
```

`miconic04.pddl` — plan de 34 pasos:

```bash
ff -o miconic.pddl -f miconic04.pddl
```

`miconic05.pddl` — plan de 46 pasos:

```bash
ff -o miconic.pddl -f miconic05.pddl
```

## Cambios respecto al original

Ninguno: los ficheros son los originales del curso.
