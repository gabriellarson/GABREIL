import numpy as np

class pokerPlayer:
    def __init__(self, name):
        self.name = name
        self.chips = None
        self.hand = [None,None]
        self.roundAction = [0]
        self.handAction = [0]
        self.previousAction = [0]
        

    def takeAction(self, gamestate, actionSpace):
        action = min(actionSpace)
        return action


    
