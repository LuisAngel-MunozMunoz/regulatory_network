###


## Pregunta 1

    -¿que funcion tiene el [TF] en regulon?
        -Respuesta: "Accede al valor del diccionario regulon cuya llave es TF
                     Key (TF) → factor de transcripción

## Pregunta 2

    -¿Que funcion tiene .join()
        Respuesta: La función join() se usa para unir varios elementos de una lista en un solo string, usando un separador.
            separador.join(lista_de_strings)
            separador → texto que se colocará entre cada elemento
            lista_de_strings → lista de textos que se quieren unir


## Pregunta 3

    - ¿Como se cambia un tipo de dato?
        Respuesta: str()

# Version 1.1

## Pregunta 1

    - Como puedo arreglar el error de no encontar el archivo

    - Sugerencia: 
        - Opcion 1: filename = "/ruta/completa/regulatory_network/data/raw/NetworkRegulatorGene.tsv"
        - Opcion 2: 
                ```txt
                    import os

                    base_dir = os.path.dirname(__file__)
                    filename = os.path.join(
                    base_dir,
                    "regulatory_network",
                    "data",
                    "raw",
                    "NetworkRegulatorGene.tsv"
                    )
                ```    
        - Opicion 3: import sys

                     filename = sys.argv[1]
    
    -Implementacion: 
                    ```txt
                    import os

                    base_dir = os.path.dirname(__file__)
                    filename = os.path.join(
                    base_dir,
                    "regulatory_network",
                    "data",
                    "raw",
                    "NetworkRegulatorGene.tsv"
                    )
                    ```
    - Que aprendi: que puedo meter rutas en una variable pero estan se van añadiendo segun donde me encuentre


## Pregunta 2

    - ¿Como puedo meter una variable a un out.write

    - Sugerencia: out.write(f"{TF}\t{total}\t{contA}\t{contR}\t{T_regul}\n")

    - Implementacion: 
                
                    ```txt
                    out.write(f"{TF}\t{total}\t{contA}\t{contR}\t{T_regul}\t{lista_genes}\n")

                    ```
    - Que aprendi: Que no puedo meter una variable solamente, debo meter o concatenar mas de una variable con \t
    
## Pregunta 3

    - ¿Como puedo corroborar que existe un archivo?

    - Sugerencia:
                ```txt
                if os.path.exists(filename):
                print("El archivo existe")
                else:
                print("El archivo no existe")
                ```
    - Implementacion:
                ```txt
                if not os.path.exists(filename):
                print("El archivo not existe)
                ```
    - Que aprendi: Que se puede usar el os.path se puede usar como argumento ademas de que no debo de identar 
                   todo, solo debo negar lo que quiero

## Pregunta 4


