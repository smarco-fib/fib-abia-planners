# SmartBus

## Qué contiene

Un autobús recoge pasajeros en sus paradas de origen y los deja en su destino. Hay pasajeros
normales y de movilidad reducida, que solo pueden ocupar plazas adaptadas. Cinco variantes del
dominio para el mismo escenario (1 bus, 14 paradas, 21 pasajeros):

| Dominio | Problema | Qué cambia | Planificador |
|---|---|---|---|
| `SmartBus-domain.pddl` | `SmartBus-prob1.pddl` | ADL con tipos; cada asiento es un objeto (butaca o plaza adaptada) | `ff` |
| `SmartBus-domainv2.pddl` | `SmartBus-prob1v2.pddl` | Otra modelización: bajar del bus y «acabar el viaje» son acciones distintas; objetivo con `forall`/`imply` | `ff` |
| `SmartBus-domain-fluents-v0.pddl` | `SmartBus-prob1-fluents-v0.pddl` | Las plazas libres son **contadores numéricos** globales (`butacasLibres`, `plazasMrLibres`) | `metric-ff -s 0` |
| `SmartBus-domain-fluents-v1.pddl` | `SmartBus-prob1-fluents-v1.pddl` | Los contadores son **por autobús** (`(butacasLibres ?bus)`) | `metric-ff -s 0` |
| `SmartBus-domain-fluents-v2.pddl` | `SmartBus-prob1-fluents-v2.pddl` | Un solo tipo `persona` y un predicado `movilidadReducida`; efectos condicionales (`when`) | `metric-ff -s 0` |

Las variantes con *fluents* usan `metric-ff -s 0`: FF no entiende `:fluents` y los problemas no
tienen `:metric` (ver [README general](../README.md#metric-ff-y--s-0)).

Para pensar: en `SmartBus-domainv2.pddl`, la acción `montar-movtotal` deja que un pasajero sin
movilidad reducida ocupe **cualquier** plaza (`?a - plaza`), también una adaptada. ¿Es lo que
queremos? ¿Cómo lo cambiarías?

## Cómo ejecutarlo

Desde esta carpeta (el número de pasos puede variar un poco según el sistema; lo importante es que el plan sea válido):

#### Dominio `SmartBus-domain.pddl`

`SmartBus-prob1.pddl` — plan de 55 pasos:

```bash
ff -o SmartBus-domain.pddl -f SmartBus-prob1.pddl
```


#### Dominio `SmartBus-domainv2.pddl`

`SmartBus-prob1v2.pddl` — plan de 77 pasos:

```bash
ff -o SmartBus-domainv2.pddl -f SmartBus-prob1v2.pddl
```


#### Dominio `SmartBus-domain-fluents-v0.pddl`

`SmartBus-prob1-fluents-v0.pddl` — plan de 55 pasos:

```bash
metric-ff -s 0 -o SmartBus-domain-fluents-v0.pddl -f SmartBus-prob1-fluents-v0.pddl
```


#### Dominio `SmartBus-domain-fluents-v1.pddl`

`SmartBus-prob1-fluents-v1.pddl` — plan de 55 pasos:

```bash
metric-ff -s 0 -o SmartBus-domain-fluents-v1.pddl -f SmartBus-prob1-fluents-v1.pddl
```


#### Dominio `SmartBus-domain-fluents-v2.pddl`

`SmartBus-prob1-fluents-v2.pddl` — plan de 55 pasos:

```bash
metric-ff -s 0 -o SmartBus-domain-fluents-v2.pddl -f SmartBus-prob1-fluents-v2.pddl
```

## Cambios respecto al original

- `SmartBus-domain-fluents-v2.pddl`: el predicado `movilidadReducida` no declaraba el tipo de su
  parámetro; ahora es `(movilidadReducida ?p - persona)`.
