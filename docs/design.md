
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
