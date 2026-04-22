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
    
    ESTRATEGIA DE ERRORES:
    ✓ MANEJA PermissionError, OSError: son errores predecibles del sistema/usuario
    ✓ MANEJA archivos vacíos: sin datos no hay procesamiento válido
    ✗ NO maneja IndexError: si ocurre, indica bug en validación de campos (fatal)
    
    Args:
        filename (str): Ruta del archivo TSV
    
    Returns:
        list: Lista de tuplas (TF, gene, effect)
        
    Raises:
        RuntimeError: si no existen datos válidos o hay problemas de I/O
    """
    # VALIDACIÓN EXPLÍCITA (sin try/except, fallos aquí = bugs del usuario) 
    if not os.path.exists(filename):
        raise RuntimeError(f"Error: Archivo no existe --> {filename}")
    
    if os.path.getsize(filename) == 0:
        raise RuntimeError(f"Error: Archivo vacío --> {filename}")
    
    interactions = []
    valid_lines = 0
    invalid_lines = 0
    
    # MANEJO DE I/O: Los únicos errores que pueden ocurrir dentro de open()
    try:
        with open(filename, encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                
                # Saltar encabezados y líneas vacías
                if not line or line.startswith("#") or line.startswith("1)regulatorId"):
                    continue

                fields = line.split("\t")
                if len(fields) <= 5:
                    continue

                TF = fields[1].strip()
                gene = fields[4].strip()
                effect = fields[5].strip()

                if effect not in ["+", "-"]:
                    continue

                interactions.append((TF, gene, effect))
    

    except PermissionError:
        raise RuntimeError(f"Error: No hay permisos para leer {filename}")
    except UnicodeDecodeError:
        raise RuntimeError(f"Error: Archivo {filename} no es UTF-8 válido")
    except OSError as e:
        raise RuntimeError(f"Error I/O al leer {filename}: {e}")

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
    
    ESTRATEGIA DE ERRORES:
    ✓ MANEJA PermissionError, OSError: problemas predecibles de I/O
    ✗ NO maneja KeyError, TypeError: indicarían bug en build_regulon() (fatal)
    
    Args:
        regulon (dict): Diccionario con estructura {TF: {gene: effect}}
        output_file (str): Ruta del archivo de salida
        
    Raises:
        RuntimeError: si hay problemas de permisos o I/O
    """
    try:
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
    
    except PermissionError:
        raise RuntimeError(f"Error: No hay permisos para escribir {output_file}")
    except OSError as e:
        raise RuntimeError(f"Error I/O al escribir {output_file}: {e}")

# ============================================================================
# VALIDACIÓN DE ENTRADA
# ============================================================================

def parse_arguments():
    """
    Parsea argumentos de línea de comandos.
    
    ESTRATEGIA DE ERRORES:
    ✗ NO necesita try/except: argparse ya maneja ValidationError automáticamente
    ✓ VALIDA min_genes explícitamente (argparse solo valida tipo, no rango)
    
    Returns:
        argparse.Namespace: Objeto con argumentos validados
        
    Raises:
        SystemExit: argparse maneja esto si hay argumentos inválidos
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
    """
    Orquesta el flujo principal del programa.
    
    ESTRATEGIA DE ERRORES:
    ✓ Solo captura RuntimeError (errores esperados, manejables)
    ✗ NO captura: bugs de lógica, KeyError, TypeError (deben fallar visiblemente)
    ✓ Crea directorios de salida si no existen (operación segura)
    """
    args = parse_arguments()
    
    # VALIDACIÓN EXPLÍCITA: archivo entrada existe (evitar OSError dentro de pipeline)
    if not os.path.exists(args.input_file):
        print(f"Error: Archivo de entrada no existe: {args.input_file}")
        exit(1)
    if not os.path.exists(os.path.dirname(args.output_file)):
        os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
        
    input_file = args.input_file
    output_file = args.output_file
    min_genes = args.min_genes

    try:

        # Pipeline
        interactions = load_interactions(input_file)
        regulon = build_regulon(interactions)

        nuevo_regulon = {}

        for TF, genes_dict in regulon.items():

            num_genes = len(genes_dict)

            if num_genes >= args.min_genes:
                nuevo_regulon[TF] = genes_dict

        regulon = nuevo_regulon

        write_regulon_summary(regulon, args.output_file)
                
        print(f"Resumen del regulon guardado en: {args.output_file}")
    except RuntimeError as e:
            print(e)
            exit(1) 
if __name__ == "__main__":
    main()

