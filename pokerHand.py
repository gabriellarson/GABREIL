class pokerHand:
    
    def __init__(self, deck, players, BBsize, logging):
        self.deck = deck.shuffle()
        self.players = players
        self.BBsize = BBsize
        self.logging = logging
        self.communityCards = [None, None, None, None, None]
        self.handEnded = False
        self.pre = True
        self.pot = 0

    def getCommunityCards(self):
        return self.communityCards

    def checkLegalAction(self, action, player): #gamestate = [self.players, self.communityCards, self.BBsize, self.pot]
        if(action[0] == "fold"):
            return True
        elif(action[0] == "raise"):
            if(action[1] > player.getChips()):
                return False
            
        return False

    def dealPre(self):
        for player in self.players:
            player.setHand(self.deck.pop(), self.deck.pop())
            print(player.name, player.hand)

    def dealFlop(self):
        self.communityCards[0] = self.deck.pop()
        self.communityCards[1] = self.deck.pop()
        self.communityCards[2] = self.deck.pop()

    def dealTurn(self):
        self.communityCards[3] = self.deck.pop()

    def dealRiver(self):
        self.communityCards[4] = self.deck.pop()

    def endHand(self):
        self.players[0].deltaChips(self.pot)
        print(self.players[0].name, "wins", self.pot, "chips")

    def bettingRound(self):
        if self.pre:
            BB = min(self.BBsize/2, self.players[0].getChips())
            self.pot += BB
            self.players[0].deltaChips(-BB)
            self.players[0].appendAction("post" + BB)

            SB = min(self.BBsize, self.players[1].getChips())
            self.pot += SB
            self.players[1].deltaChips(-SB)
            self.players[1].appendAction("post" + SB)

        gamestate = [self.players, self.communityCards, self.BBsize, self.pot]

        for player in self.players:

            legalAction = False
            while(not legalAction):
                action = player.takeAction(gamestate) #action = [fold / raise][chips];    [raise][0] is same as checking or calling, 
                legalAction = self.checkLegalAction(action, player)

            if(action[0] == "fold"):
                self.players.remove(player)
            elif(action[0] == "raise"):
                player.deltaChips(-action[1])
                self.pot += action[1]
            else:
                print("Error: invalid action")

    def playHand(self):
        if(len(self.players) > 3):
            self.dealPre()
            self.bettingRound()
            while(not self.handEnded):
                self.pre = False

                self.dealFlop()
                self.bettingRound()

                if(len(self.players) == 1):
                    break

                self.dealTurn()
                self.bettingRound()

                if(len(self.players) == 1):
                    break

                self.dealRiver()
                self.bettingRound()
            self.endHand()
