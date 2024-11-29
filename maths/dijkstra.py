from position.circuit import circuit
from position.position import position

def Treated(MatriceTreated):
    for y in range(len(MatriceTreated)):
        for x in range(len(MatriceTreated[0])):
            if(MatriceTreated[y][x] == False):
                return False
    return True

def treatable(map, CurrentY, CurrentX):
    ListeTreatable = []
    if(0 < CurrentX):
        ListeTreatable.append(position(CurrentY, CurrentX - 1, map[CurrentY][CurrentX - 1]))
    if(len(map[0]) - 1 > CurrentX):
        ListeTreatable.append(position(CurrentY, CurrentX + 1, map[CurrentY][CurrentX + 1]))
    if(0 < CurrentY):
        ListeTreatable.append(position(CurrentY - 1, CurrentX, map[CurrentY - 1][CurrentX]))
    if(len(map) - 1 > CurrentY):
        ListeTreatable.append(position(CurrentY + 1, CurrentX, map[CurrentY + 1][CurrentX]))
    return ListeTreatable

def lava(map, MatriceTreated, MatriceData):
   for y in range(len(map)):
        for x in range(len(map[0])):
            if(map[y][x] == -1):
                MatriceTreated[y][x] = True
                MatriceData[y][x].setListe(None)
                MatriceData[y][x].setValue(-1)

def unstuck(MatriceTreated, MatriceData):
    for y in range(len(MatriceTreated)):
        for x in range(len(MatriceTreated[0])):
            if(MatriceTreated[y][x] == False and type(MatriceData[y][x].valeur) == int):
                return [y, x]


def dijkstra(map, Y, X):
    CurrentX = X
    CurrentY = Y
    SizeX = len(map)
    SizeY = len(map[0])
    MatriceTreated = [[False for _ in range(SizeX)] for _ in range(SizeY)]
    MatriceData = [[circuit() for _ in range(SizeX)] for _ in range(SizeY)]
    MatriceData[Y][X].setValue(0)
    MatriceTreated[Y][X] = True
    lava(map, MatriceTreated, MatriceData)

    pas = 0 
    while(Treated(MatriceTreated) == False):
        MatriceTreated[CurrentY][CurrentX] = True
        voisins = treatable(map, CurrentY, CurrentX)
        PoidsPorte = MatriceData[CurrentY][CurrentX].valeur
        #On traite ceux autours avec le poids et le chemin que l'on possède
        for voisin in voisins:
            if(voisin.valeur != -1):
                if((MatriceData[voisin.y][voisin.x].valeur == "infinite") == False):
                    if(PoidsPorte + voisin.valeur < MatriceData[voisin.y][voisin.x].valeur):
                        MatriceData[voisin.y][voisin.x].setValue(PoidsPorte + voisin.valeur)
                        MatriceData[voisin.y][voisin.x].Liste = MatriceData[CurrentY][CurrentX].Liste + [voisin]
                else:
                        if(type(MatriceData[CurrentY][CurrentX].Liste) != list):
                            MatriceData[CurrentY][CurrentX].Liste = []
                        if(type(MatriceData[voisin.y][voisin.x].Liste) != list):
                            MatriceData[voisin.y][voisin.x].Liste = []
                        MatriceData[voisin.y][voisin.x].setValue(PoidsPorte + voisin.valeur)
                        MatriceData[voisin.y][voisin.x].Liste = MatriceData[CurrentY][CurrentX].Liste + [voisin]
        #On détermine le next step -> si il y en a pas on choisit le prochain au hasard
        #next(MatriceData, MatriceTreated, voisins, Y, X)
        PossibleNext = []
        for voisin in voisins:
            if(MatriceTreated[voisin.y][voisin.x] == False and MatriceData[voisin.y][voisin.x].valeur != -1 and MatriceData[voisin.y][voisin.x].valeur != "infinite"):
                PossibleNext.append(voisin)

        if(len(PossibleNext) > 0):
            next = None
            for possible in PossibleNext:
                if(next == None):
                    next = possible
                else:
                    #print(" NEXT : x ", MatriceData[possible.y][possible.y].valeur, " : ", MatriceData[next.y][next.y].valeur)
                    if(MatriceData[possible.y][possible.x].valeur < MatriceData[next.y][next.x].valeur):
                        next = possible
            #Definir next y / x
            CurrentY = next.y
            CurrentX = next.x
        else:
            #Cas ou pas de chemin possible
            #print("ERRRRO STUCK ")
            next = unstuck(MatriceTreated, MatriceData)
            if(next != None):
                CurrentY = next[0]
                CurrentX = next[1]
            else:
                #print("Fin : ")
                break
    return MatriceData