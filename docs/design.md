
# Algoritmo

- Lista / estructura de reguladores (sin repeticiones)
- Lista de genes del regulador (sin repeticiones)*
- Recorrer todas las interacciones(linea)
  - Para cada interacción
    - Obtener el TF
    - Obtener el gene
    - Si el TF no esta en la lista de reguladores
      - Guardar el TF en reguladores
    - Si el gene no esta en la lista de genes regulador por regulador
      - Guarda el gene asociado

- Recorrer toda la lista de los reguladores
  - Contar los genes de la lista de genes regulados por el TF
  - imprime regulador, conteo, lista de genes


# Extension



  1. Para cada TF

  2. iniciar contador de activados en 0

  3. iniciar contador de reprimidos en 0

  4. recorrer todas las interacciones

     - si la interacción pertenece a ese TF

        - si effect es +

          - aumentar activados

        - si effect es -

          - aumentar reprimidos

  5. decidir el tipo

      - si activados > 0 y reprimidos > 0

        - tipo = dual

      - si activados > 0 y reprimidos = 0

        - tipo = activador

      - si reprimidos > 0 y activados = 0

        - tipo = represor

  6. imprimir resultados



# Actualizacion 1.1 


- Leer archivo
  - recorrer líneas
  - limpiar datos
  - validar
  - extraer información
  - construir interactions
- generar salida


# Actualizacion v1.2

El programa recibira 2 argumentos desde la linea de comandos

Flujo: 

usuario -->  CLI ---> main() ---> funciones