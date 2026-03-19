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