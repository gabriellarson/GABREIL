import random
import pokerHand
import pokerPlayer

class pokerGame:

    def __init__(self, players, startingChips, handsPerLevel):
        self.players = players
        self.startingChips = startingChips
        self.handsPerLevel = handsPerLevel
        self.deck = ["As","2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks"
                    ,"Ad","2d","3d","4d","5d","6d","7d","8d","9d","Td","Jd","Qd","Kd"
                    ,"Ac","2c","3c","4c","5c","6c","7c","8c","9c","Tc","Jc","Qc","Kc"
                    ,"Ah","2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh"]


def main():
    list = [pokerPlayer("Player1"),
            pokerPlayer("Player2"),
            pokerPlayer("Player3"),
            pokerPlayer("Player4"),
            pokerPlayer("Player5"),
            pokerPlayer("Player6"),
            pokerPlayer("Player7"),
            pokerPlayer("Player8"),
            pokerPlayer("Player9")]

    game = pokerGame(list, 100, 20)

    for player in game.players:
        player.setChips(game.startingChips)
    
    BBsize = game.startingChips/100
    
    BBposition = random.randint(0,len(game.players)-1)

    while(len(game.players) > 3):
        for hand in range(game.handsPerLevel):
            hand = pokerHand(game.deck, game.players, BBposition, BBsize, False)
            hand.playHand()
        BBsize *= 2
        

if __name__ == "__main__":
    main()  


    
