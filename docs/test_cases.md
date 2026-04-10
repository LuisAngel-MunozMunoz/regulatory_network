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
AraC  1  araA
LexA  1  recA
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
CRP  3  lacZ, lacY, lacA
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
AraC  2  araA, araB
CRP  1  lacZ
LexA  1  recA
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

# Casos prueba version 1.1

1. Archivo válido (caso feliz)

- Condición
  - El archivo existe, se puede leer y contiene datos con el formato        esperado.

- Qué se prueba
  - lectura línea por línea

  - limpieza básica

  - extracción de columnas correctas

  - construcción de interactions

- Comportamiento esperado
  - el programa procesa el archivo sin errores
  - construye correctamente la lista de interacciones
  - el resto del programa puede usar esa lista sin modificarse
  - se genera el archivo de salida

2. Líneas de comentario

- Condición
  - El archivo contiene líneas que comienzan con #.

- Qué se prueba

  - que el programa distingue metadatos de datos reales

- Comportamiento esperado

  - esas líneas se ignoran completamente
  - no se intentan separar en columnas
  - no generan errores

3. Encabezado presente

- Condición
    -El archivo contiene una línea con nombres de columnas.

- Qué se prueba

    -Que el encabezado no se procese como una interacción

- Comportamiento esperado

  - el encabezado se ignora 
  - no aparece como parte de interactions

4. Línea vacía

- Condición
  - El archivo contiene una o más líneas vacías.

- Qué se prueba

  - limpieza de entrada 
  
  - manejo de líneas sin contenido

- Comportamiento esperado

  - las líneas vacías se ignoran 
  
  - no provocan errores 
  
  - no agregan elementos incorrectos a interactions

5. Valor inválido en effect

- Condición
  
  - Una fila tiene un valor distinto de + o - en la columna de efecto.

- Qué se prueba
  
  - validación de contenido

- Comportamiento esperado

  - esa fila no se incluye en interactions 
  - el programa continúa con el resto del archivo


  6. Archivo de entrada inexistente

  - Condicion
    - El archivo de entrada para el codigo no se encuentra para su uso y el codigo sabe que hacer

  - Que se prueba:
    - Que el codigo sepa que hacer en dado caso que el archivo este inexistente

  - Comportamiento esperado:
    - El programa detecta el error al abrir el archivo.
    - Se genera un mensaje de error claro.



## Command Line INterface (CLI)

Caso : Correr el programa con paso de argumentos

Entrada: 

```bash
uv run python regulon_summary.py input.txt output.txt
uv run ptython regulon_summary.py NetworkRegulatorGene.tsv tf_summary.txt
```

Resultado:
El programa lea el archivio de entrada y genere el resulrado con el nombre que se le paso como argumento