# BinPacking (empaquetado)

Planificador: **`metric-ff`** con la configuración por defecto: los problemas tienen `(:metric minimize ...)` y Metric-FF intenta encontrar un plan de coste bajo.

## Qué contiene

Colocar paquetes de distintas alturas en contenedores de altura 10 usando **el menor número de
contenedores**: los problemas incluyen `(:metric minimize (contenedoresOcupados))`.

- `BinPacking-domain-fluents-v1.pddl`: una acción, `colocar_paquete`. Al colocar el primer
  paquete en un contenedor vacío, un efecto condicional incrementa `contenedoresOcupados`.
- `BinPacking-domain-fluents-v2op.pddl`: añade `intercambiar_paquete`, que cambia de contenedor
  dos paquetes ya colocados.
- Problemas (sirven para los dos dominios): `prob1-fluents-v1-20p` (20 paquetes),
  `prob1-fluents-v2-10p` (10 paquetes, 3 contenedores), `prob2-fluents-v1`, `prob3-fluents-v1`
  (20 paquetes) y `prob4-fluents-v1-16p` (16 paquetes).

Con `v2op` el problema `prob2` tarda alrededor de un minuto: el espacio de búsqueda crece mucho
con la acción de intercambio. FF no sirve aquí: no entiende `:fluents`.

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `BinPacking-domain-fluents-v1.pddl`

`BinPacking-prob1-fluents-v1-20p.pddl` — plan de 20 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v1.pddl -f BinPacking-prob1-fluents-v1-20p.pddl
```

`BinPacking-prob1-fluents-v2-10p.pddl` — plan de 10 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v1.pddl -f BinPacking-prob1-fluents-v2-10p.pddl
```

`BinPacking-prob2-fluents-v1.pddl` — plan de 20 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v1.pddl -f BinPacking-prob2-fluents-v1.pddl
```

`BinPacking-prob3-fluents-v1.pddl` — plan de 20 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v1.pddl -f BinPacking-prob3-fluents-v1.pddl
```

`BinPacking-prob4-fluents-v1-16p.pddl` — plan de 16 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v1.pddl -f BinPacking-prob4-fluents-v1-16p.pddl
```


#### Dominio `BinPacking-domain-fluents-v2op.pddl`

`BinPacking-prob1-fluents-v1-20p.pddl` — plan de 20 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v2op.pddl -f BinPacking-prob1-fluents-v1-20p.pddl
```

`BinPacking-prob1-fluents-v2-10p.pddl` — plan de 10 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v2op.pddl -f BinPacking-prob1-fluents-v2-10p.pddl
```

`BinPacking-prob2-fluents-v1.pddl` — plan de 20 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v2op.pddl -f BinPacking-prob2-fluents-v1.pddl
```

`BinPacking-prob3-fluents-v1.pddl` — plan de 21 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v2op.pddl -f BinPacking-prob3-fluents-v1.pddl
```

`BinPacking-prob4-fluents-v1-16p.pddl` — plan de 16 pasos:

```bash
metric-ff -o BinPacking-domain-fluents-v2op.pddl -f BinPacking-prob4-fluents-v1-16p.pddl
```

## Cambios respecto al original

- Nombres de problema: los problemas de 10 y 16 paquetes se llamaban `BinPacking-20paq-6containers`
  como los de 20; ahora cada nombre describe su problema.
