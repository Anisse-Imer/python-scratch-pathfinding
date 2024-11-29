def buildMg(map):
    TailleMatrice = len(map)
    MatriceAdja = [[0 for _ in range(TailleMatrice)] for _ in range(TailleMatrice)]
    for x in range(TailleMatrice):
        for y in range(TailleMatrice):
            MatriceAdja[y][x] = map[y][x]
    return MatriceAdja