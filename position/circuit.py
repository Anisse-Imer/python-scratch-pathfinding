class circuit:
    Liste = []
    valeur = 0
    def __init__(self):
        self.valeur = "infinite"
        self.Liste = []
    def total(self):
        self.Value = 0
        for i in self.Liste:
            self.Value = self.Value + i.valeur
    def push(self, p):
        self.Liste.append(p)
    def push(self, p , value):
        self.Liste.append(p)
        if(type(self.valeur) == str):
            self.valeur = value
        elif(type(self.valeur) == int):
            self.valeur = self.valeur + value
    def setValue(self, value):
        self.valeur = value
    def setListe(self, nouveauChemin): 
        self.Liste = nouveauChemin
    def getValue(self):
        return self.valeur
    def getListe(self):
        return self.Liste