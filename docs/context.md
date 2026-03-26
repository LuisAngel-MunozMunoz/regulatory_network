# Context

Este proyecto analiza una red de regulación genética.

Los datos contienen interacciones entre factores de transcripción (TF) y genes.

Formato de los datos:

TF gene effect

Ejemplo:


```txt
AraC araA + 
AraC araB - 
LexA recA -
`````

Objetivo del programa:

Generar una tabla que indique para cada TF:

- Nombre del TF (esta solumna debe estar ordenada)
- total de genes regulados
- lista de genes regulados (ordenada).


# Extension del problema 

Además de la tabla anterior, queremos saber si cada TF es:

```txt
    activador
    represor
    dual
```



## Actualizacion 1.1

1. Leer los datos de un archivo
    1. El archivo trae 7 columnas y las que vamos a usar son: TF, gene y effect
2. Los resultados deberan mandarse a un archivo de salida