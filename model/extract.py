import position.circuit as circuit
import position.position as position
def extractPositions(sheet, Fx, Fy, Ly):
    positions = circuit.circuit()
    for y in range(Fy, Ly + 1):
        if(sheet[y][Fx + 2].value  != None):
            p = position.position(sheet[y][Fx + 1].value, sheet[y][Fx].value, sheet[y][Fx + 2].value) 
            positions.push(p, 0) 
        else:
            p = position.position(sheet[y][Fx + 1].value, sheet[y][Fx].value, 30)
            positions.push(p, 0) 
    return positions

def extractMap(sheet, Fx, Fy, Lx, Ly ):
    map = [[0 for _ in range(Lx)] for _ in range(Ly - 1)]
    for y in range(Fy, Ly + 1):
        for x in range(Fx, Lx + 1):
            map[y - 2][x - 1] = sheet[y][x].value
    return map