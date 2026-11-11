# Mundo de bloques

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

El clásico mundo de bloques: reordenar pilas de bloques sobre una mesa. Tres modelizaciones,
que se prueban con **los mismos problemas**:

- `C5-blocks-domain2ops.pddl`: 2 operadores, sin brazo: `colocar` (un bloque libre de la mesa
  encima de otro) y `despejar` (un bloque de encima de otro a la mesa).
- `C5-blocks-domain4ops.pddl`: 4 operadores con brazo robot: `pickup`, `putdown`, `stack`,
  `unstack`.
- `C5-blocks-domain6ops.pddl`: los 6 operadores juntos.

Problemas: `C5-blocks-problem1`, `2`, `2b`, `3`, `4`, `5` y `problemslides` (el de las
transparencias). Comparar el mismo problema con los tres dominios enseña cómo la modelización
cambia la longitud del plan **y la dificultad**. Con 4 operadores, ni FF ni `metric-ff -s 0`
resuelven el problema 3 (17 bloques) en 10 minutos, y `metric-ff -s 0` tampoco el problema 5: la
búsqueda (*Enforced Hill-Climbing*) se queda explorando mesetas cada vez más profundas. Con 2 o 6
operadores los mismos problemas se resuelven en un segundo o menos. ¿Por qué crees que pasa?

**`ejercicio-strips/`**: ejercicio de traducción de notación STRIPS (PRE / DEL / ADD) a PDDL.
`C5-blocks-domain4ops.str.pddl` y `C5-blocks-problem2.str` son el enunciado (a medio traducir,
**no** se pueden ejecutar); `solucion-domain4ops.pddl` y `solucion-problem2.pddl` son la solución.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `C5-blocks-domain2ops.pddl`

`C5-blocks-problem1.pddl` — plan de 11 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problem1.pddl
```

`C5-blocks-problem2.pddl` — plan de 3 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problem2.pddl
```

`C5-blocks-problem2b.pddl` — plan de 6 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problem2b.pddl
```

`C5-blocks-problem3.pddl` — plan de 34 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problem3.pddl
```

`C5-blocks-problem4.pddl` — plan de 3 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problem4.pddl
```

`C5-blocks-problem5.pddl` — plan de 22 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problem5.pddl
```

`C5-blocks-problemslides.pddl` — plan de 3 pasos:

```bash
ff -o C5-blocks-domain2ops.pddl -f C5-blocks-problemslides.pddl
```


#### Dominio `C5-blocks-domain4ops.pddl`

`C5-blocks-problem1.pddl` — plan de 20 pasos:

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problem1.pddl
```

`C5-blocks-problem2.pddl` — plan de 6 pasos:

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problem2.pddl
```

`C5-blocks-problem2b.pddl` — plan de 10 pasos:

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problem2b.pddl
```

`C5-blocks-problem3.pddl` — **no encuentra plan en 10 minutos** (ver arriba):

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problem3.pddl
```

`C5-blocks-problem4.pddl` — plan de 6 pasos:

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problem4.pddl
```

`C5-blocks-problem5.pddl` — plan de 40 pasos:

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problem5.pddl
```

`C5-blocks-problemslides.pddl` — plan de 6 pasos:

```bash
ff -o C5-blocks-domain4ops.pddl -f C5-blocks-problemslides.pddl
```


#### Dominio `C5-blocks-domain6ops.pddl`

`C5-blocks-problem1.pddl` — plan de 11 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problem1.pddl
```

`C5-blocks-problem2.pddl` — plan de 3 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problem2.pddl
```

`C5-blocks-problem2b.pddl` — plan de 6 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problem2b.pddl
```

`C5-blocks-problem3.pddl` — plan de 34 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problem3.pddl
```

`C5-blocks-problem4.pddl` — plan de 3 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problem4.pddl
```

`C5-blocks-problem5.pddl` — plan de 22 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problem5.pddl
```

`C5-blocks-problemslides.pddl` — plan de 3 pasos:

```bash
ff -o C5-blocks-domain6ops.pddl -f C5-blocks-problemslides.pddl
```


#### Dominio `solucion-domain4ops.pddl`

`solucion-problem2.pddl` — plan de 10 pasos:

```bash
cd ejercicio-strips && ff -o solucion-domain4ops.pddl -f solucion-problem2.pddl
```

## Cambios respecto al original

- `C5-blocks-problem2b.pddl` se llamaba `blocksproblem2` y `C5-blocks-problem4.pddl` se llamaba
  `blocksproblemslides`, igual que otros problemas. Ahora cada problema tiene su propio nombre.
- Añadida la solución del ejercicio en `ejercicio-strips/`.
