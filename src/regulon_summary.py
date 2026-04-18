"""
Análisis de regulones de genes.

Este módulo carga interacciones entre factores de transcripción (TF) y genes,
construye regulones agrupados por TF, y genera un resumen con estadísticas.
"""

import os, argparse


# ============================================================================
# CARGA DE DATOS
# ============================================================================

def load_interactions(filename):
    """
    Carga las interacciones desde un archivo TSV.
    
    Args:
        filename (str): Ruta del archivo TSV
    
    Returns:
        list: Lista de tuplas (TF, gene, effect)
    """
    try:
        interactions = []

        if not os.path.exists(filename):
            print("El archivo no existe")
            exit(1)

        with open(filename) as f:
            for line in f:
                line = line.strip()
                
                if not line or line.startswith("#") or line.startswith("1)regulatorId"):
                    continue

                fields = line.split("\t")
                if len(fields) <= 5:
                    continue

                TF = fields[1]
                gene = fields[4]
                effect = fields[5]

                if effect not in ["+", "-"]:
                    continue

                interactions.append((TF, gene, effect))
    

    except PermissionError:
        print("No se tienen permisos para leer el archivo")
        exit(1)

    return interactions


# ============================================================================
# PROCESAMIENTO DE DATOS
# ============================================================================

def build_regulon(interactions):
    """
    Construye un regulon agrupando genes por factor de transcripción.
    
    Args:
        interactions (list): Lista de tuplas (TF, gene, effect)
    
    Returns:
        dict: Diccionario con estructura {TF: {gene: effect, ...}, ...}
    """
    regulon = {}

    for TF, gene, effect in interactions:
        if TF not in regulon:
            regulon[TF] = {}
        regulon[TF][gene] = effect

    return regulon


# ============================================================================
# SALIDA DE DATOS
# ============================================================================

def write_regulon_summary(regulon, output_file):
    """
    Genera un archivo de resumen del regulon con estadísticas.
    
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
            
            contA = sum(1 for gene in regulon[TF] if regulon[TF][gene] == "+")
            contR = sum(1 for gene in regulon[TF] if regulon[TF][gene] == "-")
            
            if contA == 0:
                tipo_regulon = "represor"
            elif contR == 0:
                tipo_regulon = "activador"
            else:
                tipo_regulon = "dual"
            
            out.write(f"{TF}\t{total}\t{contA}\t{contR}\t{tipo_regulon}\t{lista_genes}\n")


# ============================================================================
# VALIDACIÓN DE ENTRADA
# ============================================================================

def parse_arguments():
    """
    Introduce el paso de argumentos usando argparse.
    
    args:
       Valor que tomara los argumentos de la linea de comandos
    Returns:
        argparse.Namespace: Objeto con los argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description="Lee un archivo TSV de interacciones TF-gene y genera un resumen de regulones.")

    parser.add_argument(
        "input_file", help="Archivo TSV de entrada con las interacciones TF-gene")
    parser.add_argument(
        "output_file", help="Archivo TSV de salida con el resumen de regulones")
    parser.add_argument(
        "--min_genes", type=int, default=1, help="Número mínimo de genes para incluir un TF")
    args = parser.parse_args() 

    return args
# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Orquesta el flujo principal del programa."""
    args = parse_arguments()
    
    #Validacion si existen los archivos de entrada y salida
    if not os.path.exists(args.input_file):
        print(f"Error: El archivo de entrada {args.input_file} no existe.")
        exit(1)
    if not os.path.exists(os.path.dirname(args.output_file)):
        os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
        
    interactions = load_interactions(args.input_file)
    regulon = build_regulon(interactions)
    write_regulon_summary(regulon, args.output_file)
        
    print(f"Resumen del regulon guardado en: {args.output_file}")


if __name__ == "__main__":
    main()

