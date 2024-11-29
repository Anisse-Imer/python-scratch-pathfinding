class position:
    x = 0
    y = 0
    valeur = 30
    def __init__(self, a, b):
        self.x = a
        self.y = b
    def __init__(self, a, b, value):
        self.y = a
        self.x = b     
        self.valeur = value
    def affiche(self):
        print("x : ", self.x,"y : ", self.y, " valeur : ", self.valeur)
    def dict(self):
        return {"y":self.y, "x":self.x}