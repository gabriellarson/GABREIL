import numpy as np
import random

class ActionType:
    FOLD = 0
    CALL_CHECK = 1
    BET = 2
    RAISE = 3

class pokerHand:
    
    def __init__(self, deck, players, BBindex, BBsize, logging):
        self.logging = logging
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        self.card_dict = {card: i for i, card in enumerate(deck)}
        self.card_dict['0'] = 0
        self.deck = random.sample(deck, len(deck))
        self.players = players
        self.BBsize = BBsize
        self.BBindex = BBindex
        self.communityCards = ['0','0','0','0','0']
        self.pots = [0]

        self.pre = True

    def dealPre(self):
        if self.logging: print("dealing pre")
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]


    def rank_to_int(self, rank):
        if rank == 'A':
            return 14
        elif rank == 'K':
            return 13
        elif rank == 'Q':
            return 12
        elif rank == 'J':
            return 11
        elif rank == 'T':
            return 10
        else:
            return int(rank)

    def is_straight(self, ranks):
        return all(ranks[i] == ranks[i+1] - 1 for i in range(4))

    def check_hand(self, hand):
        suits = [card[1] for card in hand]  # Change index to 1
        ranks = [self.rank_to_int(card[0]) for card in hand]

        is_flush = all(suit == suits[0] for suit in suits)
        is_straight = self.is_straight(ranks)

        rank_counts = {rank: ranks.count(rank) for rank in ranks}
        max_count = max(rank_counts.values())

        if is_flush and is_straight:
            return (8, ranks[-1])  # straight flush
        if max_count == 4:
            return (7, ranks[2])  # four of a kind
        if max_count == 3 and len(set(ranks)) == 2:
            return (6, ranks[2])  # full house
        if is_flush:
            return (5, ranks[-1])  # flush
        if is_straight:
            return (4, ranks[-1])  # straight
        if max_count == 3:
            return (3, ranks[2])  # three of a kind
        if max_count == 2:
            pair_value = max(k for k, v in rank_counts.items() if v == 2)
            if len(set(ranks)) == 3:
                return (2, pair_value)  # two pair
            else:
                return (1, pair_value)  # one pair
        return (0, ranks[-1])  # high card

    def showdown(self):
        print("showdown")
        remaining_players = [player for player in self.players if player.roundAction[-1] != -1]
        
        for player in remaining_players:
            hand = player.hand + self.communityCards
            hand = [card for card in hand if card != '0']  # Remove '0' cards
            hand.sort()
            player.handRank, player.handValue = self.check_hand(hand)

        winning_players = [remaining_players[0]]
        for player in remaining_players[1:]:
            cmp = (player.handRank - winning_players[0].handRank, player.handValue - winning_players[0].handValue)
            if cmp > (0, 0):
                winning_players = [player]
            elif cmp == (0, 0):
                winning_players.append(player)

        winners = self.distribute_winnings(winning_players)
        self.endHand(winners)
    
    def endHand(self, winners):
        if not isinstance(winners, list):
            winners = [(winners, self.pots[0])]
        for winner, winning_share in winners:
            winner.chips += winning_share
            if len(winners) > 1:
                print(winner.name, "wins", winning_share, "chips", " with ", winner.hand, " and ", self.communityCards)



    def distribute_winnings(self, winning_players):
        # Sort players by their hand strength (assuming evaluate_hand returns a higher value for stronger hands)
        ranked_players = sorted(winning_players, key=lambda player: self.check_hand(player.hand), reverse=True)

        # Go through each pot and distribute the winnings
        for pot_idx, pot_value in enumerate(self.pots):
            if pot_value == 0:
                continue

            winners = [ranked_players[0]]
            max_hand_strength = self.check_hand(ranked_players[0].hand)

            # Find all players with the same winning hand strength
            for player in ranked_players[1:]:
                hand_strength = self.check_hand(player.hand)
                if hand_strength == max_hand_strength:
                    winners.append(player)
                else:
                    break

            # Distribute the pot to the winners
            pot_share = pot_value / len(winners)
            for winner in winners:
                winner.chips += pot_share
                self.pots[pot_idx] = 0

            # Check if all pots have been distributed
            if sum(self.pots) == 0:
                break

    

    def generate_discrete_actions(self, playerActionSpaceMax, lastRaise, ceiling):
        # Generate a list of possible bet sizes
        num_bet_sizes = 3
        bet_sizes = np.linspace(ceiling, playerActionSpaceMax, num_bet_sizes)

        # Create the action space
        action_space = [(ActionType.FOLD, None), (ActionType.CALL_CHECK, None)]

        # Add bet and raise actions to the action space
        for bet_size in bet_sizes:
            if bet_size > 0:  # Ensure bet size is greater than 0
                action_space.append((ActionType.BET, bet_size))
                action_space.append((ActionType.RAISE, bet_size))

        return action_space



    def calls(self, lastRaise, player):
        if self.logging: print(player.name, " calls")
        player.roundAction.append(-2)
        amount_to_call = lastRaise - (self.pots[player.current_pot] - player.contributed[player.current_pot])
        player.chips -= amount_to_call
        self.pots[player.current_pot] += amount_to_call

    def folds(self, player):
        if self.logging: print(player.name, " folds")
        player.roundAction.append(-1)
        self.players.remove(player)

    def raises(self, action, player):
        if self.logging: print(player.name, " raises ", action[1])
        r = action[1]
        player.roundAction.append(r)
        player.chips -= r
        self.pots[player.current_pot] += r


    def calculatePlayerAction(self, lastRaise, player, playersPreviousAction, playersHandAction, playersRoundAction):
        if self.logging: print("calulating player action")
        ceiling = 0 #ceiling will be the minimum raise
        if(self.pre):
            ceiling = lastRaise + self.BBsize
        else:
            ceiling = lastRaise * 2

        playerActionSpaceMax = max(0, player.chips - (self.pots[player.current_pot] - player.contributed[player.current_pot]))

        # Generate discrete action space
        discrete_actions = self.generate_discrete_actions(playerActionSpaceMax, lastRaise, ceiling)

        gamestate = [[self.card_dict[player.hand[0]], self.card_dict[player.hand[1]]], [playersPreviousAction, playersHandAction, playersRoundAction], [self.card_dict[self.communityCards[0]], self.card_dict[self.communityCards[1]], self.card_dict[self.communityCards[2]], self.card_dict[self.communityCards[3]], self.card_dict[self.communityCards[4]]]]
        
        # Pass the discrete action space to the player
        action_idx = player.takeAction(gamestate, discrete_actions)
        action = discrete_actions[action_idx]

        return action, playerActionSpaceMax

    '''
    def calculatePlayerAction(self, lastRaise, player, playersPreviousAction, playersHandAction, playersRoundAction):
        #print("calulating player action")
        ceiling = 0 #ceiling will be the minimum raise
        if(self.pre):
            ceiling = lastRaise + self.BBsize
        else:
            ceiling = lastRaise * 2

        PlayerActionSpaceMin = -2
        if(player.chips - lastRaise <= 0):
            PlayerActionSpaceMin = -1
        playerActionSpaceMax = max(0, player.chips - (self.pot[player.current_pot] - player.contributed[player.current_pot]))
        playerActionSpace = (PlayerActionSpaceMin, playerActionSpaceMax)#[-2, -1) to call (not always available), [-1, 0) to fold, [0, maxchips] is the number of chips you want to have left after raising

        gamestate = [[self.card_dict[player.hand[0]], self.card_dict[player.hand[1]]], [playersPreviousAction, playersHandAction, playersRoundAction], [self.card_dict[self.communityCards[0]], self.card_dict[self.communityCards[1]], self.card_dict[self.communityCards[2]], self.card_dict[self.communityCards[3]], self.card_dict[self.communityCards[4]]]]
        action = player.takeAction(gamestate, playerActionSpace)
        return action, playerActionSpaceMax
    '''
    
    def calculatePreviousAction(self):
        if self.logging: print("calculating previous action")
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
        #print("calculating blinds")
        BB = min(self.BBsize/2, self.players[-1].chips)
        self.pots[self.players[-1].current_pot] += BB
        self.players[-1].chips -= BB
        self.players[-1].roundAction.append(self.players[-1].chips - BB)
        self.players[-1].contributed[self.players[-1].current_pot] = BB

        SB = min(self.BBsize, self.players[-2].chips)
        self.pots[self.players[-2].current_pot] += SB
        self.players[-2].chips -= SB
        self.players[-2].roundAction.append(self.players[-2].chips - SB)
        self.players[-2].contributed[self.players[-2].current_pot] = SB

    def playerTurn(self, player):
        if self.logging: print(player.name, "'s turn")
        lastRaise, playersPreviousAction, playersHandAction, playersRoundAction = self.calculatePreviousAction()
        action, playerActionSpaceMax = self.calculatePlayerAction(lastRaise, player, playersPreviousAction, playersHandAction, playersRoundAction)

        if action[0] == ActionType.CALL_CHECK:
            self.calls(lastRaise, player)
            self.actionCount -= 1
        elif action[0] == ActionType.FOLD:
            self.folds(player)
            self.actionCount -= 1
        elif action[0] == ActionType.BET or action[0] == ActionType.RAISE:
            self.raises(action, player)
            self.actionCount = len(self.players)
        else:
            print("Error: invalid action")
            print(action)

    def bettingRound(self):
        if self.logging: print("betting round")
        self.actionCount = len(self.players)
        actionPool = []
        #TODO action pool, sidepots
        while(self.actionCount > 0 and len(self.players) > 1):
            for player in self.players:
                if(len(self.players) == 1):
                    self.actionCount = 0
                    break
                self.playerTurn(player)

    def playHand(self):
        if self.logging: print("playing hand")
        if(len(self.players) > 3):
            self.calculateBlinds()
            self.dealPre()
            self.bettingRound()

            hand_over = False

            while not hand_over:
                if self.logging: print("Next betting round")
                self.pre = False

                self.communityCards[0] = self.deck.pop()
                self.communityCards[1] = self.deck.pop()
                self.communityCards[2] = self.deck.pop()
                self.bettingRound()
                if(len(self.players) == 1):
                    break

                self.communityCards[3] = self.deck.pop()
                self.bettingRound()
                if(len(self.players) == 1):
                    break

                self.communityCards[4] = self.deck.pop()
                self.bettingRound()
                if(len(self.players) == 1):
                    break

                hand_over = True

            self.showdown()

