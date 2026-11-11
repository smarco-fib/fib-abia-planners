# Rovers

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

El dominio Rovers (IPC-2002): robots exploradores en Marte que se desplazan, toman muestras de
suelo y roca, hacen fotografías y envían los datos al módulo de aterrizaje.

- `domain.pddl`: dominio STRIPS con tipos y nueve acciones (`navigate`, `sample_soil`,
  `sample_rock`, `drop`, `calibrate`, `take_image`, `communicate_*_data`).
- `pfile01` … `pfile20`: problemas de tamaño creciente. Los ficheros **no** tienen extensión
  `.pddl`: los planificadores no la necesitan.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `domain.pddl`

`pfile01` — plan de 10 pasos:

```bash
ff -o domain.pddl -f pfile01
```

`pfile02` — plan de 8 pasos:

```bash
ff -o domain.pddl -f pfile02
```

`pfile03` — plan de 13 pasos:

```bash
ff -o domain.pddl -f pfile03
```

`pfile04` — plan de 8 pasos:

```bash
ff -o domain.pddl -f pfile04
```

`pfile05` — plan de 22 pasos:

```bash
ff -o domain.pddl -f pfile05
```

`pfile06` — plan de 38 pasos:

```bash
ff -o domain.pddl -f pfile06
```

`pfile07` — plan de 18 pasos:

```bash
ff -o domain.pddl -f pfile07
```

`pfile08` — plan de 28 pasos:

```bash
ff -o domain.pddl -f pfile08
```

`pfile09` — plan de 33 pasos:

```bash
ff -o domain.pddl -f pfile09
```

`pfile10` — plan de 37 pasos:

```bash
ff -o domain.pddl -f pfile10
```

`pfile11` — plan de 37 pasos:

```bash
ff -o domain.pddl -f pfile11
```

`pfile12` — plan de 19 pasos:

```bash
ff -o domain.pddl -f pfile12
```

`pfile13` — plan de 46 pasos:

```bash
ff -o domain.pddl -f pfile13
```

`pfile14` — plan de 28 pasos:

```bash
ff -o domain.pddl -f pfile14
```

`pfile15` — plan de 42 pasos:

```bash
ff -o domain.pddl -f pfile15
```

`pfile16` — plan de 46 pasos:

```bash
ff -o domain.pddl -f pfile16
```

`pfile17` — plan de 49 pasos:

```bash
ff -o domain.pddl -f pfile17
```

`pfile18` — plan de 42 pasos:

```bash
ff -o domain.pddl -f pfile18
```

`pfile19` — plan de 74 pasos:

```bash
ff -o domain.pddl -f pfile19
```

`pfile20` — plan de 96 pasos:

```bash
ff -o domain.pddl -f pfile20
```

## Cambios respecto al original

Ninguno: los ficheros son los originales del curso.
