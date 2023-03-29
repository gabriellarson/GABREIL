import random

class pokerPlayer:
    def __init__(self, name):
        self.name = name
        self.chips = None
        self.hand = [None,None]
        self.roundAction = [0]
        self.handAction = [0]
        self.previousAction = [0]

    #[-2, -1) to call (not always available), [-1, 0) to fold, [0, maxchips] is the number of chips you want to have left after raising 
    def takeAction(self, gamestate, actionSpace):
        return -1


    
