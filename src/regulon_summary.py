#
#

## Representacion de datos
interactions = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-"),
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+")
]

## Para agrupar genes por tf
regulon = {}

## Recorrer las interaciones

for TF, gene, effect in interactions:
    if TF not in regulon:
        regulon[TF] = {}
    regulon[TF][gene]=effect


### imprimir

print(regulon)

### Imprimir la tabla

##### Ordenar los TFs
for TF in sorted(regulon):
    genes = regulon[TF]

##### Ordenar los genes

genes = sorted(genes)


##### Imprimir la tablita insana
print("TF 	Total genes 	Activados 	Reprimidos 	Tipo")

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
    column= "\t".join([TF, str(total), str(contA) , str(contR), T_regul])
    print(column)
        
