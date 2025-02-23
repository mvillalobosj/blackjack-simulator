import math
import os


class BettingStrategy:
    def __init__(self, gambler, table):
        self.reset()

    def reset(self):
        pass

    def get_next_bet(self):
        pass


class InteractiveBetter(BettingStrategy):

    def __init__(self, gambler, table):
        super().__init__(gambler, table)
        self.gambler = gambler
        self.table = table

    def get_next_bet(self, winnings, last_bet, base_bet):
        os.system('clear')
        print("Current Chips: {}".format(self.gambler.current_chip_count))
        print("Maximum Bet: {}".format(self.table.maximum_bet))
        next_bet = input(
            str("How much do you want to bet? (press enter to bet {}) ".format(
                base_bet)))
        if next_bet:
            if next_bet.lower() == "q":
                exit()
            return int(next_bet)
        return base_bet


class OscarSystem(BettingStrategy):

    def reset(self):
        self.total = 0
        self.modifier = 1

    def get_next_bet(self, winnings, last_bet, base_bet):
        if winnings > 0:
            self.total += self.modifier
            self.modifier += 1
        elif winnings < 0:
            self.total -= self.modifier

        if self.total >= 0:
            self.total = 0
            self.modifier = 1

        next_bet = base_bet * self.modifier

        return next_bet


class ProgressiveWinningSystem(BettingStrategy):
    def reset(self):
        self.modifier = 0

    def get_next_bet(self, winnings, last_bet, base_bet):
        if winnings > 0:
            self.modifier += 1
        elif winnings < 0:
            self.modifier = 0

        next_bet = base_bet * (2 ** self.modifier)

        return next_bet


class ProgressiveLosingSystem(BettingStrategy):
    def reset(self):
        self.modifier = 0

    def get_next_bet(self, winnings, last_bet, base_bet):
        if winnings > 0:
            self.modifier = 0
        elif winnings < 0:
            self.modifier += 1

        next_bet = base_bet * (2 ** self.modifier)

        return next_bet


class RyanSystem(BettingStrategy):
    def reset(self):
        self.modifier = 0

    def get_next_bet(self, winnings, last_bet, base_bet):
        if winnings > 0:
            self.modifier += 1
        elif winnings < 0:
            self.modifier = 0

        next_bet = base_bet + math.ceil(0.5 * base_bet * self.modifier)

        return next_bet


class ThirteenTwentySix(BettingStrategy):
    def reset(self):
        self.modifier = 0
        self.mult = [1, 3, 2, 6]

    def get_next_bet(self, winnings, last_bet, base_bet):
        if winnings > 0:
            self.modifier += 1
        elif winnings < 0:
            self.modifier = 0

        return base_bet * (self.mult[self.modifier % 4])


class AlexSystem(BettingStrategy):

    def get_next_bet(self, winnings, last_bet, base_bet):
        return base_bet
