# Torres de Hanoi

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

Las Torres de Hanoi: mover una pila de discos de un poste a otro, de uno en uno y sin poner nunca
un disco sobre otro más pequeño. Formalización de Héctor Geffner.

- `hanoi.pddl`: dominio STRIPS con una sola acción, `move`.
- `hanoi-3.pddl` … `hanoi-8.pddl`: de 3 a 8 discos. El plan óptimo tiene 2ⁿ − 1 movimientos
  (7, 15, 31, 63, 127, 255).

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `hanoi.pddl`

`hanoi-3.pddl` — plan de 7 pasos:

```bash
ff -o hanoi.pddl -f hanoi-3.pddl
```

`hanoi-4.pddl` — plan de 15 pasos:

```bash
ff -o hanoi.pddl -f hanoi-4.pddl
```

`hanoi-5.pddl` — plan de 31 pasos:

```bash
ff -o hanoi.pddl -f hanoi-5.pddl
```

`hanoi-6.pddl` — plan de 63 pasos:

```bash
ff -o hanoi.pddl -f hanoi-6.pddl
```

`hanoi-7.pddl` — plan de 127 pasos:

```bash
ff -o hanoi.pddl -f hanoi-7.pddl
```

`hanoi-8.pddl` — plan de 255 pasos:

```bash
ff -o hanoi.pddl -f hanoi-8.pddl
```

## Cambios respecto al original

Ninguno: los ficheros son los originales del curso.
