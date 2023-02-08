import numpy as np
import random

class pokerHand:
    
    def __init__(self, deck, players, BBsize, logging):
        self.deck = random.sample(deck, len(deck))
        print(self.deck)
        self.players = players
        self.BBsize = BBsize
        self.logging = logging
        self.communityCards = []
        self.handEnded = False
        self.pre = True
        self.pot = 0

    def getCommunityCards(self):
        return self.communityCards

    def dealPre(self):
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]
            print(player.name, player.hand)

    def endHand(self):
        self.players[0].chips += self.pot
        print(self.players[0].name, "wins", self.pot, "chips")

    def bettingRound(self):
        if self.pre:
            BB = min(self.BBsize/2, self.players[8].chips)
            self.pot += BB
            self.players[8].chips -= BB
            self.players[8].roundAction.append(self.players[8].chips - BB)

            SB = min(self.BBsize, self.players[7].chips)
            self.pot += SB
            self.players[7].chips -= SB
            self.players[7].roundAction.append(self.players[7].chips - SB)

        openAction = True
        while(openAction):
            for player in self.players:

                playersPreviousAction = []
                playersHandAction = []
                playersRoundAction = []
                lastRaise = 0
                for p in self.players:
                    playersPreviousAction.append(p.previousAction)
                    playersHandAction.append(p.handAction)
                    playersRoundAction.append(p.roundAction)

                    #print(p.roundAction)
                    if(p.roundAction[-1] >= 0):
                        if(p.chips - p.roundAction[-1] > lastRaise):
                            lastRaise = p.chips - p.roundAction[-1]

                ceiling = 0
                if(self.pre):
                    ceiling = lastRaise + self.BBsize
                else:
                    ceiling = lastRaise * 2

                PlayerActionSpaceMin = -2
                if(player.chips - lastRaise <= 0):
                    PlayerActionSpaceMin = -1
                playerActionSpaceMax = max(0, player.chips - ceiling)
                playerActionSpace = (PlayerActionSpaceMin, playerActionSpaceMax)#[-2, -1) to call (not always available), [-1, 0) to fold, [0, maxchips] is the number of chips you want to have left after raising

                gamestate = [player.hand, [playersPreviousAction, playersHandAction, playersRoundAction], self.communityCards]
                action = player.takeAction(gamestate, playerActionSpace)

                if(-2 <= action < -1):
                    player.roundAction.append(-2)
                    player.chips -= lastRaise
                    self.pot += lastRaise
                elif(-1 <= action < 0):
                    player.roundAction.append(-1)
                    self.players.remove(player)
                elif(0 <= action <= playerActionSpaceMax):
                    r = player.getChips() - action
                    player.roundAction.append(r)
                    player.deltaChips(r)
                    self.pot += r
                else:
                    print("Error: invalid action")


    def playHand(self):
        if(len(self.players) > 3):
            self.dealPre()
            self.bettingRound()
            while(not self.handEnded):
                self.pre = False

                self.communityCards.append(self.deck.pop())
                self.communityCards.append(self.deck.pop())
                self.communityCards.append(self.deck.pop())
                self.bettingRound()
                if(len(self.players) == 1):
                    break

                self.communityCards.append(self.deck.pop())
                self.bettingRound()
                if(len(self.players) == 1):
                    break

                self.communityCards.append(self.deck.pop())
                self.bettingRound()
            self.endHand()
