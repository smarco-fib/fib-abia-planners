# Baño compartido

Planificador: **`ff`** (FF 2.3). También funciona con `metric-ff -s 0`.

## Qué contiene

Siete personas comparten un baño con una ducha, un WC, dos lavamanos y un secador. Cada persona
quiere hacer varias cosas (ducharse, peinarse, secarse el pelo…), algunas en un orden concreto,
y cada acción necesita ciertos elementos del baño, que hay que coger y soltar.

- `ShareBath-domain.pddl`: ADL con tipos; precondiciones con `imply` y `exists`.
- `ShareBath-problem.pddl`: el objetivo (con `forall`) es que nadie quiera hacer nada más y que
  todos los elementos queden libres.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `ShareBath-domain.pddl`

`ShareBath-problem.pddl` — plan de 76 pasos:

```bash
ff -o ShareBath-domain.pddl -f ShareBath-problem.pddl
```

## Cambios respecto al original

- El nombre del problema empezaba por un número (`7pers1ducha…`): Metric-FF lo lee como un número
  y da error de sintaxis. Ahora se llama `sharebath-7pers1ducha1sanitario2lavamanos1secador`.
