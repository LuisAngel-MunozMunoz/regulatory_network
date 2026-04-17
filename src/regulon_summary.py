#
#
import os, sys

## Representacion de datos

#=================================================================================================
#Lectura del archivo y construccion de interactions
#========================================================================


#  ==================================
# Responsabilidad: leer el archivo de interacciones y construir una estructura de datos que contenga
#                  la informacion relevante para cada TF
# Entrada: archivo TSV con interacciones entre reguladores y genes
# Salida: Lista de interacciones (TF, gene, effect)
#  ==================================

def load_interactions(filename):
    """
    Carga las interacciones desde un archivo TSV
        
    Args:
        filename (str): Ruta del archivo 

    Returns:
        interactions (list): Lista de tuplas (TF, gene, effect)

    """
    interactions = []

    if not os.path.exists(filename):
        print("El archivo no existe")
        exit (1)

    with open(filename) as f:
        for line in f:
            line = line.strip()
            
            # Ignorar lineas vacias 
            if not line:
                continue

            # Ignorar comentarios
            if line.startswith("#"):
                continue

            # Ignorar encabezado 
            if line.startswith("1)regulatorId"):
                continue

            fields = line.split("\t")

            # Validar numero minimo de columnas
            if len(fields) <= 5:
                continue

            TF = fields[1]
            gene = fields[4]
            effect = fields[5]

            # Validar efecto
            if effect not in ["+", "-"]:
                continue

            interactions.append ((TF, gene, effect))

    return interactions


#  ==================================
# Construccion del regulon con informacion extra
#  ==================================

# ===================================
# Responsabilidad: generar el diccionario con las llaves y datos de cada TF con su gene y efecto
# Entrada: la lista de tuplas de las interacciones
# Salida: un diccionario con los capos solicitados
# ===================================
def build_regulon(interactions):
    """
    Construye un regulon agrupando genes por factor de transcripción
    
    Args:
        interactions (list): Lista de tuplas (TF, gene, effect)
    
    Returns:
        regulon (dict): Diccionario con estructura {TF: {gene: effect, ...}, ...}
    """
    regulon = {}

    for TF, gene, effect in interactions:
        if TF not in regulon:
            regulon[TF] = {}
        regulon[TF][gene] = effect

    return regulon


# =================================================================
# Generacion de la salida
# =================================================================



#  ==================================
# Responsabilidad: Hacer la tabla en un archivo de salida que tenga los datos de cada TF con su gene, efecto, total etc
# Entrada: El diccionario de diccionario
# Salida: Un archivo con todo lo solicitado
#  ==================================
def write_regulon_summary(regulon, output_file):
    """
    Genera un archivo de resumen del regulon con estadísticas
    
    Args:
        regulon (dict): Diccionario del regulon
        output_file (str): Ruta del archivo de salida
    """
    with open(output_file, "w") as out:
        out.write("TF\tTotal genes\tActivados\tReprimidos\tTipo\tGenes\n")

        for TF in sorted(regulon):
            genes = sorted(regulon[TF])
            total = len(genes)
            lista_genes = ", ".join(genes)
            contA = 0
            contR = 0
            
            for gene in regulon[TF]:
                efecto = regulon[TF][gene]
                if efecto == "+":
                    contA += 1
                else:
                    contR += 1
            
            if contA == 0:
                T_regul = "represor"
            elif contR == 0:
                T_regul = "activador"
            else:
                T_regul = "dual"
            
            out.write(f"{TF}\t{total}\t{contA}\t{contR}\t{T_regul}\t{lista_genes}\n")


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    filename = os.path.join(BASE_DIR, "..", "data", "raw", "NetworkRegulatorGene.tsv")

    # Cargar interacciones
    interactions = load_interactions(filename)
    
    # Construir regulon
    regulon = build_regulon(interactions)
    
    # Definir archivo de salida
    output_file = os.path.join(BASE_DIR, "..", "results", "regulon_summary_output.txt")
    
    # Escribir resumen
    write_regulon_summary(regulon, output_file)
    
    print(f"Resumen del regulon guardado en: {output_file}")


if __name__ == "__main__":
    main()

