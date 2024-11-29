import json
import model.extract as extract
import position.position as position

from openpyxl import Workbook, load_workbook
from itertools import combinations,permutations
import maths.dijkstra as dijkstra
#---------------------------------------
#Récupération des données / construction DataSet2
f = open('DataSet1.json')
dataPoints = json.load(f)
f.close()

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

##INTERET
ListePinter = []
for i in range(len(Pinter.Liste)):
    ListePinter.append(Pinter.Liste[i])
for i in ListePinter:
    #i.affiche()
    None

#Interset combinaisons :
temp = []
PinterCombinaisons = []
for i in range(len(ListePinter) + 1):
    temp.append(combinations(ListePinter, i))

for i in temp:
    for y in i:
        PinterCombinaisons.append(list(y))

ToutesCombinaisons = []
for obl in ToutesCombinaisonsStrat:
    for inter in PinterCombinaisons:
        ToutesCombinaisons.append(obl + inter)

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

#Transforme une liste de postions en liste en liste de dictionnaires contenant des positions -> càd les chemins
for y1 in range(len(Matrice)):
    for x1 in range(len(Matrice)):
        for y2 in range(len(Matrice)):
            for x2 in range(len(Matrice)):
                if(type(Matrice[y1][x1][y2][x2].Liste) == list):
                    provisoire = []
                    for p in Matrice[y1][x1][y2][x2].Liste:
                        provisoire.append({"y": p.y,"x": p.x})
                    Chemin[y1][x1][y2][x2] = provisoire

##On a récupéré toutes les combinaisons, on va essayer de les parcourir
#-> Combinaisons
#-> points stratégiques
#-> 
#-> s'arrête à ces conditions : 
#--------> tous points obigatoires atteint 
#--------> le prochain pas est négatif
#   Remarque : algo intéressant -> plusieurs couches de recherche de rentabiité

#Données complètes dijkstra + affichage

def bestPath(ListeProchaine, PositionActuel, MatriceDijkstra):
    BestNextPosition = ListeProchaine[0]
    for proposition in ListeProchaine:
        if(proposition.valeur - MatriceDijkstra[PositionActuel.y - 1][PositionActuel.y - 1][proposition.y- 1][proposition.x- 1].valeur > BestNextPosition.valeur - MatriceDijkstra[PositionActuel.y- 1][PositionActuel.y- 1][BestNextPosition.y- 1][BestNextPosition.x- 1].valeur):
            BestNextPosition = proposition
    BestNextPosition.valeur = BestNextPosition.valeur - MatriceDijkstra[PositionActuel.y - 1][PositionActuel.y - 1][BestNextPosition.y - 1][BestNextPosition.x - 1].valeur
    return BestNextPosition


def copyListofPosition(Liste):
    newList = []
    for posi in Liste:
        newList.append(position.position(posi.y, posi.x, posi.valeur))
    return newList

DataMeilleurChemin = []
for combi in ToutesCombinaisons:
    uneCombinaison = copyListofPosition(combi)
    MonChemin = []
    PstratObligatoire = [Pstrat.Liste[0], Pstrat.Liste[2], Pstrat.Liste[5], Pstrat.Liste[6]]
    ystart = 19
    xstart = 11 
    CurrentPosition = position.position(ystart,xstart,0)
    LastValue = 0
    NextPosition = None
    TotalPoint = 0
    while(len(PstratObligatoire) != 0 and len(uneCombinaison) > 0):
        NextPosition = bestPath(uneCombinaison, CurrentPosition, Matrice)
        for x in Chemin[CurrentPosition.y - 1][CurrentPosition.x - 1][NextPosition.y - 1][NextPosition.x - 1] :
            MonChemin.append(x)
        CurrentPosition = NextPosition
        uneCombinaison.remove(CurrentPosition)
        if(PstratObligatoire.count(CurrentPosition)):
            PstratObligatoire.remove(CurrentPosition)
        TotalPoint += CurrentPosition.valeur
    DataMeilleurChemin.append({
        "y-start" :ystart,
        "x-start" :xstart,
        "y-end":CurrentPosition.y,
        "x-end":CurrentPosition.x,
        "point" : TotalPoint,
        "chemin" : MonChemin
    })


MeilleurChemin = DataMeilleurChemin[0]
for chemin in DataMeilleurChemin :
    if(MeilleurChemin["point"] < chemin["point"]):
        MeilleurChemin = chemin

for x in MeilleurChemin["chemin"]:
    x["y"] += 1
    x["x"] += 1

# Serializing json
json_object = json.dumps(MeilleurChemin, indent=4)
 
# Writing to sample.json
with open("DataSetMeilleurChemin.json", "w") as outfile:
    outfile.write(json_object)