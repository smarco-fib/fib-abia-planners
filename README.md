# fib-abia-planners

Los planificadores **FF 2.3** y **Metric-FF 2.1** (Jörg Hoffmann) listos para usar en
Windows, Linux y macOS, con los ejemplos de planificación de la asignatura ABIA (UPC).
No hace falta compilar nada.

## Instalación

```bash
python -m pip install --upgrade pip
```

```bash
pip install fib-abia-planners
```

Se recomienda instalarlo en un entorno virtual (`python -m venv`): la
[guía del alumnado](https://github.com/smarco-fib/fib-abia-planners/blob/main/docs/GUIA_ALUMNOS.md)
explica cómo hacerlo en Windows, macOS y Linux.

Comprueba que funciona:

```bash
fib-abia-planners selftest
```

## Uso

Copia los ejemplos a una carpeta tuya y prueba uno:

```bash
fib-abia-planners examples mis-ejemplos
```

```bash
cd mis-ejemplos/hanoi
```

```bash
ff -o hanoi.pddl -f hanoi-3.pddl
```

- `ff`: FF 2.3, para dominios sin números (STRIPS y ADL).
- `metric-ff`: Metric-FF 2.1, para dominios con números (`:fluents`) y métricas (`:metric`).
  Si el problema no tiene `:metric`, usa `metric-ff -s 0` (ver `README.md` de los ejemplos).

Los dos programas aceptan exactamente las mismas opciones que los originales.

## Si algo falla

```bash
fib-abia-planners selftest --all
```

```bash
fib-abia-planners info
```

y envía la salida completa al profesorado de la asignatura.

## Licencia

GPL versión 2 o posterior. FF y Metric-FF son © Universidad Albert Ludwig de Friburgo
(Jörg Hoffmann). Ver `LICENSE`, `NOTICE` y, para los cambios respecto al código
original, `PATCHES.md`.
