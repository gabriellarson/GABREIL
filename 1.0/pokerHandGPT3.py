import numpy as np
import random

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
        self.pot = [0]*8

        self.pre = True

    def dealPre(self):
        #print("dealing pre")
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]

    def is_straight(self, ranks):
        return all(ranks[i] == ranks[i+1] - 1 for i in range(4))

    def check_hand(self, hand):
        suits = [card[1] for card in hand]  # Change index to 1
        ranks = [int(card[0]) for card in hand]

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
    
    def calculate_pots(self):
        # Create a list of all contributions from all players
        contributions = []
        for player in self.players:
            contributions.extend(player.contributed)

        # Sort the contributions in descending order
        contributions.sort(reverse=True)

        # Create a list of the unique contributions
        unique_contributions = list(set(contributions))

        # Create a dictionary to store the pots and their contributors
        pots = {c: [] for c in unique_contributions}

        # Iterate through the unique contributions
        for i, c in enumerate(unique_contributions):
            # Find the players whose contributions are equal to or greater than the current contribution
            contributing_players = [p for p in self.players if p.contributed.count(c) > i]
            # Sort the contributing players by hand rank
            contributing_players.sort(key=lambda p: p.handRank, reverse=True)
            # Add the contributing players to the current pot
            for player in contributing_players:
                pots[c].append(player)

        # Create a list of all side pots
        side_pots = []
        for i, c in enumerate(unique_contributions):
            # Find the players whose contributions are greater than the current contribution
            contributing_players = [p for p in self.players if p.contributed.count(c) > i + 1]
            if len(contributing_players) > 0:
                # Calculate the size of the side pot
                side_pot_size = c - unique_contributions[i + 1]
                # Create a dictionary to store the side pot and its contributors
                side_pot = {'size': side_pot_size, 'contributors': []}
                # Add the contributing players to the side pot
                for player in contributing_players:
                    side_pot['contributors'].append(player)
                    player_contributions = [c for c in player.contributed if c > unique_contributions[i + 1]]
                    player_contributions.sort(reverse=True)
                    for contribution in player_contributions:
                        if side_pot_size > 0:
                            if side_pot_size >= contribution - unique_contributions[i + 1]:
                                side_pot_size -= contribution - unique_contributions[i + 1]
                            else:
                                side_pot_size = 0
                # Add the side pot to the list of side pots
                side_pots.append(side_pot)

        # Add the side pots to the pots dictionary
        for side_pot in side_pots:
            pots[unique_contributions[-1]] += side_pot['contributors']
            for winner in pots[unique_contributions[-1]]:
                winner.chips += side_pot['size'] / len(pots[unique_contributions[-1]])

        return pots

    def showdown(self):
        #print("showdown")
        for player in self.players:
            hand = player.hand + self.communityCards
            hand = [card for card in hand if card != '0']  # Remove '0' cards
            hand.sort()
            player.handRank, player.handValue = self.check_hand(hand)

        pots = self.calculate_pots()
        winners = []
        for pot, pot_contributions in pots.items():
            # Find the highest hand rank among the contributing players
            max_hand_rank = max(p.handRank for p in pot_contributions)
            # Find the winning players with the highest hand rank
            winning_players = [p for p in pot_contributions if p.handRank == max_hand_rank]

            for player in pot_contributions:
                if player.handRank == max_hand_rank:
                    winners.append(player)
            # Calculate the share of the pot each winner gets
            winning_share = pot / len(winners)
            # Distribute the winnings to the winners
            for winner in winners:
                winner.chips += winning_share
                if len(winners) > 1:
                    print(winner.name, "wins", winning_share, "chips with", winner.hand, "and", self.communityCards)
        self.endHand(winners)
    
    def endHand(self, winners):
        if not isinstance(winners, list):
            winners = [(winners, self.pot[0])]
        for winner, winning_share in winners:
            winner.chips += winning_share



    def distribute_winnings(self, winning_players):
        pots = self.pot.copy()
        winners = []

        # Sort the pots in descending order of size
        sorted_pots = sorted([(i, pot) for i, pot in enumerate(pots) if pot > 0], key=lambda x: x[1], reverse=True)

        # Distribute the winnings for each pot separately
        for i, pot in sorted_pots:
            winning_pot_players = [p for p in winning_players if p.contributed[i] > 0]
            if len(winning_pot_players) == 0:
                continue

            # Calculate the total contribution of the winning players to the pot
            total_contribution = sum(p.contributed[i] for p in winning_pot_players)

            # Calculate the share of each winning player based on their contribution
            shares = [(p, p.contributed[i] / total_contribution) for p in winning_pot_players]

            # Sort the shares in descending order of size
            sorted_shares = sorted(shares, key=lambda x: x[1], reverse=True)

            # Distribute the pot among the winning players based on their share
            for j, (p, share) in enumerate(sorted_shares):
                if j == 0 or share == sorted_shares[j-1][1]:
                    winners.append((p, share * pot))
                else:
                    remaining_pot = pot - sum(w[1] for w in winners)
                    winners.append((p, remaining_pot))

        return winners


    def calls(self, lastRaise, player):
        #print(player.name, " calls")
        player.roundAction.append(-2)
        player.chips -= lastRaise
        self.pot += lastRaise

    def folds(self, player):
        #print(player.name, " folds")
        player.roundAction.append(-1)
        self.players.remove(player)

    def raises(self, action, player):
        #print(player.name, " raises ", player.chips - action)
        r = player.chips - action
        player.roundAction.append(r)
        player.chips -= r
        self.pot[player.current_pot] += r

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
    
    def calculatePreviousAction(self):
        #print("calculating previous action")
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
        self.pot[self.players[-1].current_pot] += BB
        self.players[-1].chips -= BB
        self.players[-1].roundAction.append(self.players[-1].chips - BB)
        self.players[-1].contributed[self.players[-1].current_pot] = BB

        SB = min(self.BBsize, self.players[-2].chips)
        self.pot[self.players[-2].current_pot] += SB
        self.players[-2].chips -= SB
        self.players[-2].roundAction.append(self.players[-2].chips - SB)
        self.players[-2].contributed[self.players[-2].current_pot] = SB

    def playerTurn(self, player):
        #print(player.name, "'s turn")
        lastRaise, playersPreviousAction, playersHandAction, playersRoundAction = self.calculatePreviousAction()
        action, playerActionSpaceMax = self.calculatePlayerAction(lastRaise, player, playersPreviousAction, playersHandAction, playersRoundAction)

        if(-2 <= action < -1):
            self.calls(lastRaise, player)
            self.actionCount -= 1
        elif(-1 <= action < 0):
            self.folds(player)
            self.actionCount -= 1
        elif(0 <= action <= playerActionSpaceMax):
            self.raises(action, player)
            self.actionCount = len(self.players)
        else:
            print("Error: invalid action")
            print(action)

    def bettingRound(self):
        #print("betting round")
        self.actionCount = len(self.players)
        actionPool = []
        #TODO action pool, sidepots
        while(self.actionCount > 0):
            for player in self.players:
                if(len(self.players) == 1):
                    self.actionCount = 0
                    break
                self.playerTurn(player)

    def playHand(self):
        #print("playing hand")
        if(len(self.players) > 3):
            self.calculateBlinds()
            self.dealPre()
            self.bettingRound()

            while(True):
                self.pre = False

                self.communityCards[0] = self.deck.pop()
                self.communityCards[1] = self.deck.pop()
                self.communityCards[2] = self.deck.pop()
                self.bettingRound()
                if(len(self.players) == 1):
                    winner = self.players[0]
                    break

                self.communityCards[3] = self.deck.pop()
                self.bettingRound()
                if(len(self.players) == 1):
                    winner = self.players[0]
                    break

                self.communityCards[4] = self.deck.pop()
                self.bettingRound()
                if(len(self.players) == 1):
                    winner = self.players[0]
                    break

                winner = self.showdown()
            self.endHand(winner)
