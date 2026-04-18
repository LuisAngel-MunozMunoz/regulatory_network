import argparse


parser = argparse.ArgumentParser(description="Resumen de regulones a partir de un archivo de interacciones")

# definir argumentos

parser.add_argument("input_file", help="Archivo TSV de entrada con interacciones TF-gene")
parser.add_argument("output_file", help="Archivo TSV de salida con resumen de regulones")
parser.add_argument("--min_genes",type=int, default=1, help="Numero minimo de genes para incluir un TF")


args = parser.parse_args()

print (args)

print (f"Archivo de entrada: {args.input_file}")
print (f"Archivo de salida: {args.output_file}")
print (f"Numero minimo de genes: {args.min_genes}")
