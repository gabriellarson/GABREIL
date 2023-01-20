class pokerGame:

    def __init__(self, players, startingBB, handsPerLevel):
        self.players = players
        self.startingBB = startingBB
        self.handsPerLevel = handsPerLevel
        self.deck = ["As","2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks","Ad","2d","3d","4d","5d","6d","7d","8d","9d","Td","Jd","Qd","Kd","Ac","2c","3c","4c","5c","6c","7c","8c","9c","Tc","Jc","Qc","Kc","Ah","2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh"]

    def deal():
        deck.shuffle()
        for player in players:
            player.hand.append(deck.pop())
            player.hand.append(deck.pop())
            player.hand.sort()
            print(player.name, player.hand)
