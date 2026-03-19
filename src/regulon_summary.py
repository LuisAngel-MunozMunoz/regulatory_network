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
        regulon[TF] = []
    regulon[TF].append(gene)


### imprimir

print(regulon)

### Imprimir la tabla

##### Ordenar los TFs
for TF in sorted(regulon):
    genes = regulon[TF]

##### Ordenar los genes

genes = sorted(genes)


##### Imprimir la tablita insana


for TF in sorted(regulon):
    genes = sorted(regulon[TF])
    total = len(genes)
    lista_genes = ", ".join(genes)
    print(TF, total, lista_genes)

