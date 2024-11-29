import position.circuit as circuit
import position.position as position
import model.extract as extract
import maths.dijkstra as dijkstra
from openpyxl import Workbook, load_workbook

#Partie math compo de toutes les possibilités
from itertools import combinations
from itertools import permutations

import json

from itertools import chain, combinations

book = load_workbook('Map.xlsx')
sheet = book.active

#On récupère la map indéxée à (-1) sur y/x
map = extract.extractMap(sheet, 1, 2, 20, 21)
#On récupère les positions strat/inter
Pstrat = extract.extractPositions(sheet, 22, 4, 10)
Pinter = extract.extractPositions(sheet, 25, 4, 10)

PstratObligatoire = [Pstrat.Liste[0], Pstrat.Liste[2], Pstrat.Liste[5], Pstrat.Liste[6]]
PstratNonObligatoire = [Pstrat.Liste[1], Pstrat.Liste[3], Pstrat.Liste[4]]
temp = []
PstratNonObligatoireCombinaisons = []
"""
    #-- Non obligatoire
##Détermine toutes les combinaisons / de toutes les tailles
for i in range(0, len(PstratNonObligatoire) + 1):
    temp.append(combinations(PstratNonObligatoire, i))
##Transformation de tuple vers liste
for i in temp:
    for y in i:
        PstratNonObligatoireCombinaisons.append(list(y))
#On va mélanger composer toutes les combinaisons donc : obligatoire + [toutes les combinaisons]
ToutesCombinaisonsStrat = []
for i in PstratNonObligatoireCombinaisons:
    ToutesCombinaisonsStrat.append(PstratObligatoire + i)
    print("Combi NEW composé :  PstratObligatoire ")
    for y in PstratObligatoire + i:
        y.affiche()

##INTERET
print("Interest")
ListePinter = []
for i in range(len(Pinter.Liste)):
    ListePinter.append(Pinter.Liste[i])
for i in ListePinter:
    #i.affiche()
    None

print("Interset combinaisons :")
temp = []
PinterCombinaisons = []
for i in range(len(ListePinter) + 1):
    temp.append(combinations(ListePinter, i))

for i in temp:
    for y in i:
        PinterCombinaisons.append(list(y))

for i in PinterCombinaisons:
    print("#")
    for p in i:
        p.affiche()

ToutesCombinaisons = []
for obl in ToutesCombinaisonsStrat:
    for inter in PinterCombinaisons:
        ToutesCombinaisons.append(obl + inter)
        print("Combinaison finale : ")
        for y in obl + inter:
            y.affiche()
"""
"""
#ARRANGEMENT - abandon - 
temp = []
ToutesArrangements = []
for Combi in ToutesCombinaisons:
    temp.append(permutations(Combi))
for i in temp:
    for arr in i:
        print("Arrangement")
        for p in list(arr):
            p.affiche()
"""
            
#Données complètes dijkstra + affichage

map = extract.extractMap(sheet, 1, 2, 20, 21)
#Test génération toutes positions
Matrice = [[[] for _ in range(len(map))] for _ in range(len(map[0]))]
for y in range(len(map)):
    for x in range(len(map[0])):
        #print("Dijkstra : ", y, " : ", x)
        Matrice[y][x] = dijkstra.dijkstra(map, y, x)

taille = len(map)
Chemin = [[[[list for _ in range(taille)] for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]

for y1 in range(len(Matrice)):
    for x1 in range(len(Matrice)):
        for y2 in range(len(Matrice)):
            for x2 in range(len(Matrice)):
                if(type(Matrice[y1][x1][y2][x2].Liste) == list):
                    provisoire = []
                    for p in Matrice[y1][x1][y2][x2].Liste:
                        provisoire.append({"y": p.y,"x": p.x})
                    Chemin[y1][x1][y2][x2] = provisoire

StratStart = []
for pStart in Pstrat.Liste:
    for pEnd in Pstrat.Liste:
        StratStart.append({
        "y1": pStart.y,
        "x1": pStart.x,
        "y2": pEnd.y,
        "x2": pEnd.x,
        "cost": Matrice[pStart.y][pStart.x][pEnd.y][pEnd.x].valeur,
        "path": Chemin[pStart.y][pStart.x][pEnd.y][pEnd.x]
    })

InterInter = []
for pStart in Pinter.Liste:
    for pEnd in Pinter.Liste:
        InterInter.append({
        "y1": pStart.y,
        "x1": pStart.x,
        "y2": pEnd.y,
        "x2": pEnd.x,
        "cost": Matrice[pStart.y][pStart.x][pEnd.y][pEnd.x].valeur,
        "path": Chemin[pStart.y][pStart.x][pEnd.y][pEnd.x]
    })

StratInter = []
for pStart in Pinter.Liste:
    for pEnd in Pstrat.Liste:
        StratInter.append({
        "y1": pStart.y,
        "x1": pStart.x,
        "y2": pEnd.y,
        "x2": pEnd.x,
        "cost": Matrice[pStart.y][pStart.x][pEnd.y][pEnd.x].valeur,
        "path": Chemin[pStart.y][pStart.x][pEnd.y][pEnd.x]
    })
        
for pStart in Pstrat.Liste:
    for pEnd in Pinter.Liste:
        StratInter.append({
        "y1": pStart.y,
        "x1": pStart.x,
        "y2": pEnd.y,
        "x2": pEnd.x,
        "cost": Matrice[pStart.y][pStart.x][pEnd.y][pEnd.x].valeur,
        "path": Chemin[pStart.y][pStart.x][pEnd.y][pEnd.x]
    })

DataStat1 = {"strat-strat": StratStart, "inter-inter":InterInter, "strat-inter":StratInter}

# Serializing json
json_object = json.dumps(DataStat1, indent=4)
 
# Writing to sample.json
with open("DataSet1.json", "w") as outfile:
    outfile.write(json_object)