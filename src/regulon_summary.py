import os

#  ==================================
# Responsabilidad: leer el archivo de interacciones y construir una estructura de datos 
# Entrada: archivo TSV con interacciones entre reguladores y genes
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
        print(f"Error: el archivo {filename} no existe")
        return interactions

    with open(filename) as f:
        for line in f:
            line = line.strip()
            
            # Ignorar líneas vacías 
            if not line:
                continue

            # Ignorar comentarios
            if line.startswith("#"):
                continue

            # Ignorar encabezado 
            if line.startswith("1)regulatorId"):
                continue

            fields = line.split("\t")

            # Validar número mínimo de columnas
            if len(fields) <= 5:
                continue

            TF = fields[1]
            gene = fields[4]
            effect = fields[5]

            # Validar efecto
            if effect not in ["+", "-"]:
                continue

            interactions.append((TF, gene, effect))
    
    return interactions


#  ==================================
# Responsabilidad: generar el diccionario con las llaves y datos de cada TF con su gene y efecto
# Entrada: la lista de tuplas de las interacciones
# Salida: un diccionario con los capos solicitados
# ===================================

def build(interactions):
    """
    Construye un diccionario con regulones (TF -> genes mapping)
    
    Args:
        interactions (list): Lista de tuplas (TF, gene, effect)
    
    Returns:
        dict: Diccionario donde las claves son TFs y valores son dicts de genes
    """
    regulon = {}
    
    for TF, gene, effect in interactions:
        if TF not in regulon:
            regulon[TF] = {}
        regulon[TF][gene] = effect
    
    return regulon




#  ==================================
# Responsabilidad: Generar el archivo de salida con resumen del regulon
# Entrada: El diccionario de regulon
# Salida: Un archivo con los datos de cada TF con su gene, efecto, total, etc
#  ==================================

def write_regulon_summary(regulon, output_file=None):
    """
    Escribe un resumen del regulon en un archivo de salida
    
    Args:
        regulon (dict): Diccionario con los regulones
        output_file (str): Ruta del archivo de salida. Si es None, usa la ruta por defecto.
    """
    if output_file is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(BASE_DIR, "..", "results", "regulon_summary_output.txt")
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w") as out:
        out.write("TF\tTotal genes\tActivados\tReprimidos\tTipo\tGenes\n")
        
        for TF in sorted(regulon):
            genes = sorted(regulon[TF])
            total = len(genes)
            lista_genes = ", ".join(genes)
            
            contA = 0  # contador de activadores
            contR = 0  # contador de represores
            
            for gene in regulon[TF]:
                efecto = regulon[TF][gene]
                if efecto == "+":
                    contA += 1
                else:
                    contR += 1
            
            # Determinar tipo de factor de transcripción
            if contA == 0:
                T_regul = "represor"
            elif contR == 0:
                T_regul = "activador"
            else:
                T_regul = "dual"
            
            out.write(f"{TF}\t{total}\t{contA}\t{contR}\t{T_regul}\t{lista_genes}\n")
    
    print(f"Resumen escrito en {output_file}")


#  ==================================
# MAIN: Flujo principal
#  ==================================

if __name__ == "__main__":
    # Construir ruta del archivo de datos
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, "..", "data", "raw", "NetworkRegulatorGene.tsv")
    
    # Cargar interacciones
    interactions = load_interactions(filename)
    print(f"Interacciones cargadas: {len(interactions)}")
    
    if not interactions:
        print("No hay interacciones que procesar")
        exit(1)
    
    # Construir regulon
    regulon = build(interactions)
    print(f"Regulones construidos: {len(regulon)}")
    
    # Escribir resumen
    write_regulon_summary(regulon)



