from pokerHand import pokerHand
import copy

class pokerGame:

    def __init__(self, players, startingChips, handsPerLevel):
        self.players = players
        for player in self.players:
            player.chips = startingChips
        self.startingChips = startingChips
        self.handsPerLevel = handsPerLevel
        self.deck = ["As","2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks"
                    ,"Ad","2d","3d","4d","5d","6d","7d","8d","9d","Td","Jd","Qd","Kd"
                    ,"Ac","2c","3c","4c","5c","6c","7c","8c","9c","Tc","Jc","Qc","Kc"
                    ,"Ah","2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh"]
        

    def play(self):
        BBsize = self.startingChips/100
        BBindex = 0
        numHands = 0
        while(len(self.players) > 3):
            for hands in range(self.handsPerLevel):
                if(len(self.players) <= 3):
                    break
                self.checkForLoser()
                BBindex+=1
                if(BBindex >= len(self.players)):
                    BBindex = 0

                logs = True
                
                hand = pokerHand(copy.copy(self.deck), copy.copy(self.players), BBindex, BBsize, logs)
                hand.playHand()
                numHands+=1
            BBsize *= 5

        print(numHands)
        print("Winner: " + self.players[0].name)
        print("Winner: " + self.players[1].name)
        print("Winner: " + self.players[2].name)


    def checkForLoser(self):
        if(len(self.players) > 3):
            for player in self.players:
                if(player.chips <= 0):
                    self.players.remove(player)


    
