class handHistory:
    def __init__(self):
        self.history = [None]

    #entry format:
    #[Position(positions away from BB, 0 being the BB, 9 meaning player is OUT of the tournament),
    #player1action[
    #  preflop,flop,turn,river    #preflop/flop/turn/river = [actions[], amounts[]]   
    #                                                             #actions = [fold, call (calling 0 == check), raise]  
    #                                                              #amounts = [amount of chips bet/raised, 0 if not a raise]
    # ]
    # player2action
    # ...
    # player9action
    # ]
    def add(self, entry):
        self.history.append(entry)

    def get(self):
        return self.history

    def clear(self):
        self.history = [None]



