#
#
import os
## Representacion de datos


interactions = []

# Lectura de datos desde un archivo TSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(BASE_DIR, "..", "data", "raw", "NetworkRegulatorGene.tsv")

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



## Para agrupar genes por tf
regulon = {}

## Recorrer las interaciones

for TF, gene, effect in interactions:
    if TF not in regulon:
        regulon[TF] = {}
    regulon[TF][gene]=effect


### imprimir


### Imprimir la tabla

##### Ordenar los TFs
for TF in sorted(regulon):
    genes = regulon[TF]

##### Ordenar los genes

genes = sorted(genes)

with open("results/regulon_summary_output.txt", "w") as out:
    out.write("TF 	Total genes 	Activados 	Reprimidos 	Tipo")


##### Imprimir la tablita insana


    for TF in sorted(regulon):
        genes = sorted(regulon[TF])
        total = len(genes)
        lista_genes = ", ".join(genes)
        contA=0
        contR=0
        for gene in regulon[TF]:
            efecto=regulon[TF][gene]
            if efecto == "+":
                contA +=1 
            else: 
                contR += 1
            if contA == 0: 
                T_regul="represor"
            elif contR == 0:
                T_regul="activador"
            else:
                T_regul="dual"
            
            
            
            out.write(f"{TF}\t{total}\t{contA}\t{contR}\t{T_regul}\t{lista_genes}\n")
        
