# Ordenar un vector

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

Ordenar los valores de un vector intercambiándolos. Cuatro modelizaciones:

- `C5-vector-v1.pddl`: sin tipos; `swap` intercambia los valores de dos posiciones **contiguas**
  (`next`). Problemas `C5-prob-vector-v1` (3 valores) y `v1-10val` (10 valores).
- `C5-vector-typed-v1.1.pddl`: lo mismo **con tipos** (`pos`, `valor`). Problemas
  `C5-prob-vector-Typed-v1.1` y `Typed-v1.1-10val`.
- `C5-vector-typed-v1.2.pddl`: con tipos y ADL; el objetivo se describe con un predicado `target`
  y `swap` solo hace intercambios que colocan un valor en su sitio (en cualquier par de
  posiciones, no solo contiguas). El problema `Typed-v1.2-10val` expresa el objetivo con
  `forall`/`imply`. Problemas `C5-prob-vector-Typed-v1.2` y `Typed-v1.2-10val`.
- `C5-vector-v2.pddl`: el vector como lista enlazada (`izquierda ?a ?b`), con dos elementos
  «fantasma» en los extremos. Problemas `C5-prob-vector-v2` (3 valores), `v2-5val` y `v2-10val`.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `C5-vector-v1.pddl`

`C5-prob-vector-v1.pddl` — plan de 2 pasos:

```bash
ff -o C5-vector-v1.pddl -f C5-prob-vector-v1.pddl
```

`C5-prob-vector-v1-10val.pddl` — plan de 22 pasos:

```bash
ff -o C5-vector-v1.pddl -f C5-prob-vector-v1-10val.pddl
```


#### Dominio `C5-vector-typed-v1.1.pddl`

`C5-prob-vector-Typed-v1.1.pddl` — plan de 2 pasos:

```bash
ff -o C5-vector-typed-v1.1.pddl -f C5-prob-vector-Typed-v1.1.pddl
```

`C5-prob-vector-Typed-v1.1-10val.pddl` — plan de 22 pasos:

```bash
ff -o C5-vector-typed-v1.1.pddl -f C5-prob-vector-Typed-v1.1-10val.pddl
```


#### Dominio `C5-vector-typed-v1.2.pddl`

`C5-prob-vector-Typed-v1.2.pddl` — plan de 2 pasos:

```bash
ff -o C5-vector-typed-v1.2.pddl -f C5-prob-vector-Typed-v1.2.pddl
```

`C5-prob-vector-Typed-v1.2-10val.pddl` — plan de 8 pasos:

```bash
ff -o C5-vector-typed-v1.2.pddl -f C5-prob-vector-Typed-v1.2-10val.pddl
```


#### Dominio `C5-vector-v2.pddl`

`C5-prob-vector-v2.pddl` — plan de 2 pasos:

```bash
ff -o C5-vector-v2.pddl -f C5-prob-vector-v2.pddl
```

`C5-prob-vector-v2-5val.pddl` — plan de 8 pasos:

```bash
ff -o C5-vector-v2.pddl -f C5-prob-vector-v2-5val.pddl
```

`C5-prob-vector-v2-10val.pddl` — plan de 24 pasos:

```bash
ff -o C5-vector-v2.pddl -f C5-prob-vector-v2-10val.pddl
```

## Cambios respecto al original

- Nombres de problema: el número del nombre ahora coincide con el número de valores
  (`vector3`, `vector5`, `vector10`).
- Dominios con tipos: `?y -pos` corregido a `?y - pos`.
