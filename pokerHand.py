import numpy as np
import random

class pokerHand:
    
    def __init__(self, deck, players, BBindex, BBsize, logging):
        self.deck = random.sample(deck, len(deck))
        #print(self.deck)
        self.players = players
        self.BBsize = BBsize
        self.logging = logging
        self.communityCards = []
        self.handEnded = False
        self.pre = True
        self.pot = 0
        self.BBindex = BBindex

    def dealPre(self):
        print("dealing pre")
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]

    def showdown(self):
        for player in self.players:
            print(player.name, player.hand, player.chips)
            hand = player.hand + self.communityCards
            hand.sort()

            #check for straight flush
            if(hand[0][0] == hand[1][0] and hand[1][0] == hand[2][0] and hand[2][0] == hand[3][0] and hand[3][0] == hand[4][0]):
                if(hand[4][1] == hand[3][1] + 1 and hand[3][1] == hand[2][1] + 1 and hand[2][1] == hand[1][1] + 1 and hand[1][1] == hand[0][1] + 1):
                    player.handRank = 8
                    player.handValue = hand[4][1]
                    continue

            #check for four of a kind
            if(hand[0][0] == hand[1][0] and hand[1][0] == hand[2][0] and hand[2][0] == hand[3][0]):
                player.handRank = 7
                player.handValue = hand[2][1]
                continue
            if(hand[1][0] == hand[2][0] and hand[2][0] == hand[3][0] and hand[3][0] == hand[4][0]):
                player.handRank = 7
                player.handValue = hand[3][1]
                continue

            #check for full house
            if(hand[0][0] == hand[1][0] and hand[1][0] == hand[2][0] and hand[3][0] == hand[4][0]):
                player.handRank = 6
                player.handValue = hand[2][1]
                continue
            if(hand[0][0] == hand[1][0] and hand[2][0] == hand[3][0] and hand[3][0] == hand[4][0]):
                player.handRank = 6
                player.handValue = hand[4][1]
                continue

            #check for flush
            if(hand[0][0] == hand[1][0] and hand[1][0] == hand[2][0] and hand[2][0] == hand[3][0] and hand[3][0] == hand[4][0]):
                player.handRank = 5
                player.handValue = hand[4][1]
                continue

            #check for straight
            if(hand[4][1] == hand[3][1] + 1 and hand[3][1] == hand[2][1] + 1 and hand[2][1] == hand[1][1] + 1 and hand[1][1] == hand[0][1] + 1):
                player.handRank = 4
                player.handValue = hand[4][1]
                continue

            #check for three of a kind
            if(hand[0][0] == hand[1][0] and hand[1][0] == hand[2][0]):
                player.handRank = 3
                player.handValue = hand[2][1]
                continue
            if(hand[1][0] == hand[2][0] and hand[2][0] == hand[3][0]):
                player.handRank = 3
                player.handValue = hand[3][1]
                continue
            if(hand[2][0] == hand[3][0] and hand[3][0] == hand[4][0]):
                player.handRank = 3
                player.handValue = hand[4][1]
                continue

            #check for two pair
            if(hand[0][0] == hand[1][0] and hand[2][0] == hand[3][0]):
                player.handRank = 2
                player.handValue = hand[3][1]
                continue
            if(hand[0][0] == hand[1][0] and hand[3][0] == hand[4][0]):
                player.handRank = 2
                player.handValue = hand[4][1]
                continue
            if(hand[1][0] == hand[2][0] and hand[3][0] == hand[4][0]):
                player.handRank = 2
                player.handValue = hand[4][1]
                continue

            #check for one pair
            if(hand[0][0] == hand[1][0]):
                player.handRank = 1
                player.handValue = hand[1][1]
                continue
            if(hand[1][0] == hand[2][0]):
                player.handRank = 1
                player.handValue = hand[2][1]
                continue
            if(hand[2][0] == hand[3][0]):
                player.handRank = 1
                player.handValue = hand[3][1]
                continue
            if(hand[3][0] == hand[4][0]):
                player.handRank = 1
                player.handValue = hand[4][1]
                continue

            #check for high card
            player.handRank = 0
            player.handValue = hand[4][1]

            #if handRank is tied, check handValue
            for p in self.players:
                if(p.handRank == player.handRank):
                    if(p.handValue > player.handValue):
                        player.handRank = -1
                        player.handValue = -1
                        break
        #return winning player
        return max(self.players, key=lambda x: (x.handRank, x.handValue))

    def endHand(self):
        self.players[0].chips += self.pot
        print(self.players[0].name, "wins", self.pot, "chips", " with ", self.players[0].hand, " and ", self.communityCards)

    def calls(self, lastRaise, player):
        print(player.name, " calls")
        player.roundAction.append(-2)
        player.chips -= lastRaise
        self.pot += lastRaise

    def folds(self, player):
        print(player.name, " folds")
        player.roundAction.append(-1)
        self.players.remove(player)

    def raises(self, action, player):
        print(player.name, " raises ", action)
        r = player.chips - action
        player.roundAction.append(r)
        player.chips -= r
        self.pot += r

    def calculatePlayerAction(self, lastRaise, player, playersPreviousAction, playersHandAction, playersRoundAction):
        ceiling = 0 #ceiling will be the minimum raise
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
        return action, playerActionSpaceMax
    
    def calculatePreviousAction(self):
        playersPreviousAction = []
        playersHandAction = []
        playersRoundAction = []
        lastRaise = 0
        for p in self.players:
            playersPreviousAction.append(p.previousAction)
            playersHandAction.append(p.handAction)
            playersRoundAction.append(p.roundAction)

            if(p.roundAction[-1] >= 0):#if last action was putting in chips
                if(p.chips - p.roundAction[-1] > lastRaise):#if the amount of chips was greater than the previous raise
                    lastRaise = p.chips - p.roundAction[-1]
        return lastRaise, playersPreviousAction, playersHandAction, playersRoundAction
    
    def calculateBlinds(self):
        BB = min(self.BBsize/2, self.players[-1].chips)
        self.pot += BB
        self.players[-1].chips -= BB
        self.players[-1].roundAction.append(self.players[-1].chips - BB)

        SB = min(self.BBsize, self.players[-2].chips)
        self.pot += SB
        self.players[-2].chips -= SB
        self.players[-2].roundAction.append(self.players[-2].chips - SB)
        return BB, SB

    def bettingRound(self):
        openAction = True
        while(openAction):
            for player in self.players:
                lastRaise, playersPreviousAction, playersHandAction, playersRoundAction = self.calculatePreviousAction()

                action, playerActionSpaceMax = self.calculatePlayerAction(lastRaise, player, playersPreviousAction, playersHandAction, playersRoundAction)

                if(-2 <= action < -1):
                    self.calls(lastRaise, player)
                elif(-1 <= action < 0):
                    self.folds(player)
                elif(0 <= action <= playerActionSpaceMax):
                    self.raises(action, player)
                else:
                    print("Error: invalid action")
                    print(action)


    def playHand(self):
        if(len(self.players) > 3):
            self.calculateBlinds()
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
                if(len(self.players) == 1):
                    break
                self.showdown()
            self.endHand()
