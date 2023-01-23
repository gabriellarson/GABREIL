class pokerPlayer:
    def __init__(self, name):
        self.name = name
        self.chips = None
        self.hand = [None,None]
        self.previousAction = None

    def deltaChips(self, chipsDelta):
        self.chips += chipsDelta

    def setChips(self, chips):
        self.chips = chips

    def getChips(self):
        return self.chips

    def setHand(self, card1, card2):
        self.hand = [card1, card2]
        self.hand.sort()
    
    def getHand(self):
        return self.hand

    def getName(self):
        return self.name

    def takeAction(self, gamestate):
        action = "fold"
        self.appendAction(action)
        return action

    def getPreviousAction(self):
        return self.previousAction

    def appendAction(self, action):
        self.previousAction.append(action)
    
