from copy import deepcopy
import os
import random

SOFT = 'soft'
HARD = 'hard'
PAIR = 'pair'
BLACKJACK = 'blackjack'

HIT = 'h'
STAND = 's'
SPLIT = 'p'
DOUBLE_DOWN = 'd'

face_cards = ['10', 'J', 'Q', 'K']


hard_moves = {
     1: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     2: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     3: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     4: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     5: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     6: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     7: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     8: ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # nopep8
     9: ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    10: ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h'],  # nopep8
    11: ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd'],  # nopep8
    12: ['h', 'h', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    13: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    14: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    15: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    16: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    17: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # nopep8
    18: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # nopep8
    19: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # nopep8
    20: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's']   # nopep8
}

soft_moves = {
    11: ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd'],  # nopep8
    13: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    14: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    15: ['h', 'h', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    16: ['h', 'h', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    17: ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    18: ['d', 'd', 'd', 'd', 'd', 's', 's', 'h', 'h', 'h'],  # nopep8
    19: ['s', 's', 's', 's', 'd', 's', 's', 's', 's', 's'],  # nopep8
    20: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's']   # nopep8
}

pair_moves = {
     2: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # nopep8
     4: ['p', 'p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h'],  # nopep8
     6: ['p', 'p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h'],  # nopep8
     8: ['h', 'h', 'h', 'p', 'p', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    10: ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h'],  # nopep8
    12: ['p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h', 'h'],  # nopep8
    14: ['p', 'p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h'],  # nopep8
    16: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # nopep8
    18: ['p', 'p', 'p', 'p', 'p', 's', 'p', 'p', 's', 's'],  # nopep8
    20: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's']   # nopep8
}


def average(l):
    return sum(l) / len(l)


class DeckEmpty(Exception):
    pass


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def get_value(self):
        if self.number == 'A':
            return 1
        elif self.number in face_cards:
            return 10
        else:
            return int(self.number)

    def __str__(self):
        return "{}{}".format(self.number, self.suit)


class Deck:
    def __init__(self, num_decks):
        self.suits = '♠♥♦♣'
        self.numbers = \
            ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.base_deck = self._get_sorted_decks(num_decks)
        self.shuffled_deck = []

    def shuffle(self):
        shuffled_deck = []
        deck = deepcopy(self.base_deck)
        shuffled_deck = [
            deck.pop(random.randint(0, len(deck) - 1)) for i in range(len(deck))]

   #     while len(deck) > 0:
   #         shuffled_deck.append(
   #3             deck.pop(random.randint(0, len(deck) - 1))
   #         )

        self.shuffled_deck = shuffled_deck

    def deal(self):
        if len(self.shuffled_deck) <= 0:
            raise DeckEmpty
        return deepcopy(self.shuffled_deck.pop())

    def _get_sorted_decks(self, num_decks):
        sorted_decks = []
        for number in range(num_decks):
            for suit in self.suits:
                for number in self.numbers:
                    sorted_decks.append(Card(suit, number))
        return sorted_decks

    def __str__(self):
        return '\n'.join(str(card) for card in self.deck)


class Hand:
    def __init__(self, cards, bet_value=0):
        self.cards = cards
        self._locked = False
        self._additional_cards = 0
        self._busted = False
        self._double_down = False
        self._blackjack = False
        self.calculate_value()
        self.bet_value = bet_value

    def reset_additional_cards(self):
        self._additional_cards = 0

    def hand_value(self):
        return self._hand_value

    def calculate_value(self):
        self._busted = False
        hand_type = HARD

        if len(self.cards) == 2:
            if self._is_pair(self.cards):
                hand_type = PAIR
            elif self._is_blackjack(self.cards):
                self._locked = True
                self._blackjack = True
                self._hand_value = (BLACKJACK, 21)
                return

        has_ace, value = self._get_value(self.cards)
        if has_ace and value <= 11:
            if hand_type == HARD:
                hand_type = SOFT
            value += 10
        if value >= 21:
            self._locked = True
            if value > 21:
                self._busted = True

        self._hand_value = (hand_type, value)

    def lock(self):
        self._locked = True

    @property
    def double_down(self):
        return self._double_down

    @double_down.setter
    def double_down(self, value):
        self._double_down = value

    def add_card(self, card):
        self._additional_cards += 1
        self.cards.append(card)
        self.calculate_value()

    def remove_card(self):
        self._additional_cards -= 1
        card = self.cards.pop()
        self.calculate_value()
        return card

    @property
    def added_cards(self):
        return self._additional_cards

    @property
    def locked(self):
        return self._locked

    @property
    def blackjack(self):
        return self._blackjack

    @property
    def busted(self):
        return self._busted

    @staticmethod
    def _is_pair(cards):
        return (cards[0].number == cards[1].number)

    def _is_blackjack(self, cards):
        if self.added_cards > 0:
            return False
        return ((cards[0].number in face_cards and cards[1].number == 'A') or
                (cards[1].number in face_cards and cards[0].number == 'A'))

    @staticmethod
    def _get_value(cards):
        value = 0
        has_ace = False
        for card in cards:
            value += card.get_value()
            if card.number == 'A':
                has_ace = True
        return (has_ace, value)

    def print_hand(self, hidden=False):
        if hidden:
            cards = deepcopy(self.cards)
            cards[0].number = 'X'
            cards[0].suit = 'X'
        else:
            cards = self.cards

        hand = ' '.join(str(card) for card in cards)
        hand_type, value = self._hand_value
        if hidden:
            value = self.cards[1].get_value()
            if value == 1:
                hand += ' ({} or {})'.format(value, value + 10)
            else:
                hand += ' ({})'.format(value)
        else:
            if hand_type == SOFT:
                hand += ' ({} {} or {})'.format(hand_type, value - 10, value)
            else:
                hand += ' ({} {})'.format(hand_type, value)
        if self.busted:
            hand += ' BUSTED '
        elif self.blackjack:
            hand += ' BLACKJACK! '
        return hand

    def __str__(self):
        return self.print_hand()


class Character:
    def __init__(self, deck):
        self.hands = []
        self.deck = deck
        self.move_map = {
            HIT: self.hit,
            STAND: self.stand,
            SPLIT: self.split,
            DOUBLE_DOWN: self.double_down
        }
        self.moves = []

    def make_move(self, move, hand_number):
        self.moves.append(move)
        self.move_map[move](hand_number)

    def hit(self, hand_number):
        self.hands[hand_number].add_card(self.deck.deal())

    def stand(self, hand_number):
        self.hands[hand_number].lock()

    def split(self, hand_number):
        hand = self.hands[hand_number]
        self.add_hand([hand.remove_card()])
        self.hands[hand_number].reset_additional_cards()

    def double_down(self, hand_number):
        self.hit(hand_number)
        hand = self.hands[hand_number]
        hand.lock()
        hand.double_down = True
        hand.bet_value += self.current_bet

    def add_hand(self, cards):
        self.hands.append(Hand(cards, self.make_bet()))
        self.hands[-1].reset_additional_cards()

    def add_card_to_hand(self, hand_number):
        self.hands[hand_number].add_card(self.deck.deal())

    def pending_hands(self):
        return [index
                for index, hand in enumerate(self.hands)
                if not hand.locked]

    def __str__(self):
        return '\n\n'.join(['-- Hand {} Bet: ${} --\n{}'.format(
                            index + 1, hand.bet_value, hand)
                            for index, hand in enumerate(self.hands)])


class Dealer(Character):
    def allowed_moves(self, hand_number):
        hand = self.hands[hand_number]
        hand_type, value = hand.hand_value()
        if hand.busted or hand.locked:
            return []
        if value < 17 or value == 17 and hand_type == SOFT:
            return [HIT]
        else:
            return [STAND]

    def make_bet(self):
        return 0

    def print_dealer(self, hidden):
        return str(self.hands[0].print_hand(hidden))

    def __str__(self):
        return str(self.hands[0])


class Player(Character):
    def __init__(self, deck, chip_count, current_bet):
        super(Player, self).__init__(deck)
        self.chip_count = chip_count
        self._current_bet = current_bet

    def make_bet(self):
        self.chip_count -= self.current_bet
        return self.current_bet

    @property
    def current_bet(self):
        return self._current_bet

    def allowed_moves(self, hand_number):
        hand = self.hands[hand_number]
        hand_type, value = hand.hand_value()
        if hand.busted or hand.locked:
            return []

        allowed_moves = [HIT, STAND]

        if self.chip_count - self.current_bet > 0:
            if hand_type == PAIR:
                allowed_moves.append(SPLIT)

            if self.hands[hand_number].added_cards == 0:
                allowed_moves.append(DOUBLE_DOWN)

        return allowed_moves

    def suggested_move(self, hand_number, dealer_number):
        hand = self.hands[hand_number]
        hand_type, value = hand.hand_value()
        dealer_index = 0
        if dealer_number == 'A':
            dealer_index = 9
        elif dealer_number in face_cards:
            dealer_index = 8
        else:
            dealer_index = int(dealer_number) - 2

        if hand_type == HARD:
            return hard_moves[value][dealer_index]
        elif hand_type == SOFT:
            return soft_moves[value][dealer_index]
        elif hand_type == PAIR:
            return pair_moves[value][dealer_index]


class Game:
    def __init__(self, deck, chip_count, bet):
        self.deck = deck
        self.chip_count = chip_count
        self.bet = bet

    def print_board(self, hidden=False):
        os.system('clear')
        print("Chip Count: {}".format(self.chip_count))
        print("Dealer")
        print(self.dealer.print_dealer(hidden))
        print("\n----\n")
        print("Player")
        print(self.player)
        print("----")

    def get_move(self, current_hand, allowed_moves, suggested_move):
        print("Current Hand: {}".format(current_hand + 1))
        print("Allowed Moves: {}".format("".join(allowed_moves)))
        print("Suggested Move: {}".format(suggested_move))
        print("----")
        move = input("What's your Move?: ")
        while move not in allowed_moves:
            print("invalid selection")
            move = input("What's your Move?: ")
        return move

    def make_move(self, move, current_hand):
        self.player.make_move(move, current_hand)

    def get_current_hand(self):
        possible_hands = self.player.pending_hands()
        if len(possible_hands) > 0:
            return possible_hands[0]
        else:
            return None

    def setup_game(self, base_bet):
        self.dealer = Dealer(self.deck)
        self.player = Player(self.deck, self.chip_count, base_bet)
        self.player.add_hand([self.deck.deal()])
        self.dealer.add_hand([self.deck.deal()])
        self.player.add_card_to_hand(0)
        self.dealer.add_card_to_hand(0)
        self.player.hands[0].reset_additional_cards()
        self.dealer.hands[0].reset_additional_cards()
        self.player.hands[0].calculate_value()
        self.dealer.hands[0].calculate_value()

    def run_game(self):
        self.setup_game(self.bet)
        hand = self.get_current_hand()
        # self.print_board(hidden=True)
        while hand is not None and self.dealer.hands[0].blackjack is False:
            # allowed_moves = self.player.allowed_moves(hand)
            suggested_move = self.player.suggested_move(
                hand, self.dealer.hands[0].cards[1].number)
            move = suggested_move  # self.get_move(hand, allowed_moves, suggested_move)
            self.make_move(move, hand)
            hand = self.get_current_hand()
            # self.print_board(hidden=True)
        while self.dealer.allowed_moves(0):
            self.dealer.make_move(self.dealer.allowed_moves(0)[0], 0)
        # self.print_board()
        winnings = self.get_winnings()
        # print("Winnings: {}".format(winnings))
        # input("")
        return winnings

    def get_winnings(self):
        total_winnings = 0
        dealer_hand = self.dealer.hands[0]
        for hand in self.player.hands:
            if hand.busted:
                total_winnings -= hand.bet_value
            elif hand.blackjack:
                total_winnings += int(hand.bet_value * 1.5)
            elif dealer_hand.busted:
                total_winnings += int(hand.bet_value)
            else:
                _, hand_value = hand.hand_value()
                _, dealer_value = dealer_hand.hand_value()
                if hand_value > dealer_value:
                    total_winnings += hand.bet_value
                elif hand_value < dealer_value:
                    total_winnings -= hand.bet_value
        return total_winnings


class Reporter:
    def __init__(self, system_name):
        self.system_name = system_name
        self.reset_overall_report()

    def reset_overall_report(self):
        self.total_game_count = 0
        self.win_count = 0
        self.lose_count = 0
        self.reset_bet_report(0)
        self.bet_summary = []

    def reset_bet_report(self, bet):
        self.bet_game_count = 0
        self.bet = bet
        self.game_count = 0
        self.bankrupt = 0
        self.hit_goal = 0
        self.hit_maximum_bet = 0
        self.max_chip_count = 0
        self.games_to_goal = []
        self.games_to_bankrupt = []

    def print_bet_report(self):
        print("Bet: {}".format(self.bet))
        print("Bankrupt Count: {}".format(self.bankrupt))
        print("Average games to bankrupt: {}".format(average(self.games_to_bankrupt)))
        print("Goal Gount: {}".format(self.hit_goal))
        print("Average games to goal: {}".format(average(self.games_to_goal)))
        print("Game Count: {}".format(self.bet_game_count))
        print("Hit Maximum Bet: {}".format(self.hit_maximum_bet))
        print("Maximum Chip Count: {}".format(self.max_chip_count))
        print("-----------------------------")

    def print_overall_report(self):
        most_goals = 0
        best_summary = {}
        for summary in self.bet_summary:
            if summary['goal_percent'] > most_goals:
                best_summary = summary
                most_goals = summary['goal_percent']

        print("System: {}".format(self.system_name))
        print("Best Bet: {}".format(best_summary['bet']))
        print("Goal Percentage: {}".format(best_summary['goal_percent']))
        print("Avg Games to Goal: {}".format(best_summary['games_to_goal']))
        print("Total Game Count: {}".format(self.total_game_count))
        print("Win Count: {}".format(self.win_count))
        print("Lose Count: {}".format(self.lose_count))
        print("Win Percentage: {}".format(self.win_count / (self.win_count + self.lose_count)))
        print("-----------------------------")

    def record_game_results(self, winnings, chip_count, is_max_bet):
        self.max_chip_count = max(self.max_chip_count, chip_count)
        if winnings > 0:
            self.win_count += 1
        elif winnings < 0:
            self.lose_count += 1
        if is_max_bet:
            self.hit_maximum_bet += 1
        self.game_count += 1

    def record_session_results(self, chip_count):
        if chip_count <= 0:
            self.bankrupt += 1
            self.games_to_bankrupt.append(self.game_count)
        else:
            self.hit_goal += 1
            self.games_to_goal.append(self.game_count)
        self.bet_game_count += self.game_count

    def record_bet_results(self, chip_count):
        bet_summary = {
            'bet': self.bet,
            'goal_percent': (self.hit_goal / (self.hit_goal + self.bankrupt)) * 100,
            'games_to_goal': average(self.games_to_goal)
        }
        self.bet_summary.append(bet_summary)

    def reset_session(self):
        self.total_game_count += self.game_count
        self.game_count = 0


class BettingStragegy:
    def __init__(self):
        self.reset()

    def reset(self):
        pass

    def get_next_bet(self):
        pass


class OscarSystem(BettingStragegy):
    def reset(self):
        self.total = 0
        self.modifier = 1

    def get_next_bet(self, winnings, last_bet, maximum_bet, base_bet):
        if winnings > 0:
            self.total += self.modifier
            self.modifier += 1
        elif winnings < 0:
            self.total -= self.modifier

        if self.total >= 0:
            self.total = 0
            self.modifier = 1
        is_max_bet = False
        if base_bet * self.modifier > maximum_bet:
            self.modifier = maximum_bet / base_bet
            is_max_bet = True

        next_bet = base_bet * self.modifier
        return next_bet, is_max_bet


class ProgressiveWinningSystem(BettingStragegy):
    def reset(self):
        self.modifier = 1

    def get_next_bet(self, winnings, last_bet, maximum_bet, base_bet):
        if winnings > 0:
            self.modifier += 1
        elif winnings < 0:
            self.modifier = 1

        next_bet = base_bet * (2 ** self.modifier)
        is_max_bet = False
        if next_bet > maximum_bet:
            next_bet = maximum_bet
            is_max_bet = True

        return next_bet, is_max_bet


class ProgressiveLosingSystem(BettingStragegy):
    def reset(self):
        self.modifier = 1

    def get_next_bet(self, winnings, last_bet, maximum_bet, base_bet):
        if winnings > 0:
            self.modifier = 1
        elif winnings < 0:
            self.modifier += 1

        next_bet = base_bet * (2 ** self.modifier)
        is_max_bet = False
        if next_bet > maximum_bet:
            next_bet = maximum_bet
            is_max_bet = True

        return next_bet, is_max_bet


class Gambler:
    def __init__(self, base_chip_count, winnings_goal, bet_unit):
        self.base_chip_count = base_chip_count
        self.winnings_goal = winnings_goal
        self.goal = base_chip_count + winnings_goal
        self.chip_count = self.base_chip_count
        self.bet_unit = bet_unit

    def reset(self):
        self.chip_count = self.base_chip_count

    def done(self):
        return self.chip_count <= 0 or self.chip_count >= self.goal


class Table:
    def __init__(self, maximum_bet, ante):
        self.maximum_bet = maximum_bet
        self.ante = ante


def run():
    gambler = Gambler(base_chip_count=1000, winnings_goal=100, bet_unit=5)
    table = Table(maximum_bet=500, ante=0.5)
    deck = Deck(6)

    betting_systems = [
        OscarSystem(),
        ProgressiveLosingSystem(),
        ProgressiveWinningSystem()
    ]

    for better in betting_systems:
        reporter = Reporter(better.__class__.__name__)
        reporter.reset_overall_report()
        bet = 0
        while bet < 100:
            bet = bet + gambler.bet_unit
            reporter.reset_bet_report(bet)

            for i in range(1000):
                reporter.reset_session()
                better.reset()
                gambler.reset()
                next_bet = bet
                while not gambler.done():
                    if len(deck.shuffled_deck) < 52:
                        deck.shuffle()

                    gambler.chip_count -= table.ante
                    if next_bet > gambler.chip_count:
                        next_bet = gambler.chip_count
                    game = Game(deck, gambler.chip_count, next_bet)
                    winnings = game.run_game()
                    gambler.chip_count += winnings

                    next_bet, is_max_bet =\
                        better.get_next_bet(winnings, next_bet, table.maximum_bet, bet)
                    reporter.record_game_results(
                        winnings, gambler.chip_count, is_max_bet)

                reporter.record_session_results(gambler.chip_count)

            reporter.record_bet_results(gambler.chip_count)
            # reporter.print_bet_report()

        reporter.print_overall_report()

if __name__ == '__main__':
    run()
