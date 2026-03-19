# Casos de prueba

## Caso 1

    Entrada:

```txt
AraC araA +
AraC araB -
```

    Salida esperada:

```txt
AraC 2 araA, araB
```
    Despues de la prueba:
    - Si salio eso

## Caso 2

Entrada:

```txt
AraC araA +
LexA recA -
```

Salida esperada:

```txt
AraC 	1 	araA
LexA 	1 	recA
```

    Despues de la prueba:
    - Si salio eso

## Caso 3

Entrada:

```txt
CRP lacZ +
CRP lacY +
CRP lacA +
```

Salida esperada:

```txt
CRP 	3 	lacZ, lacY, lacA
```
    Despues de la prueba:
    - Si salio eso

## Caso 4

Entrada

```txt
AraC araA +
AraC araB -
CRP lacZ +
LexA recA -
```

Salida esperada:

```txt
AraC 	2 	araA, araB
CRP 	1 	lacZ
LexA 	1 	recA
```

    Despues de la prueba:
    - Si salio eso


# Extension 

Datos 1

interactions = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-")
]

Salida :
AraC    2       1       1       dual
LexA    1       0       1       represor

Datos 2

interactions = [
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+"),
    ("CRP", "lacA", "+")
]

Salida:
    CRP     3       3       0       activador

Datos 3

interactions = [
    ("LexA", "recA", "-"),
    ("LexA", "umuC", "-"),
    ("AraC", "araE", "+"),
    ("AraC", "araA", "-")
]

Salida:

    AraC    2       1       1       dual
    LexA    2       0       2       represor