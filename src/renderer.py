from copy import deepcopy
from time import sleep
import os


class Renderer:
    def render_deal(self):
        pass

    def pre_game_render(self):
        pass

    def render_game(self):
        pass

    def post_game_render(self, winnings):
        pass


class InteractiveRenderer(Renderer):
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer

    def pre_game_render(self):
        os.system('clear')
        self.print_board(hidden=True)

    def render_game(self):
        self.print_board(hidden=True)

    def post_game_render(self, winnings):
        self.print_board(hidden=False)
        if winnings > 0:
            print("\n\n:-) You Won {}!".format(winnings))
        elif winnings < 0:
            print("\n\n:-( You Lost {}".format(winnings * -1))
        else:
            print("\n\n:-| Push! You got your money back")

        input("\n\nPress Enter to play again")

    def render_deal(self):
        self.print_board(hidden=True)
        sleep(1)

    def print_board(self, hidden=False):
        os.system('clear')
        print("Dealer")
        print(self.print_hand(self.dealer.hand, hidden))
        print("\n--------------------------------------\n")
#        print("Player")
        print(self.print_player(self.player))
        print("----")
        print("(Chips: ${}   Total Bet: ${})".format(
            self.player.current_chip_count,
            self.player.total_bet))

    def print_player(self, player):
        hand_layout = '    ( ${} )\n\n -- Hand {} --\n{}'
        return '\n\n'.join([
            hand_layout.format(
                hand.bet_value,
                hand.hand_number,
                self.print_hand(hand))
            for hand in player.hands])

    def print_hand(self, hand, hidden=False):
        if not hand:
            return ''
        if hidden:
            cards = deepcopy(hand.cards)
            cards[0].number = '▓'
            cards[0].suit = '▓'
        else:
            cards = hand.cards

        print_hand = ' '.join(str(card) for card in cards)
        hand_type, value = hand.hand_value

        if hidden and len(hand.cards) > 1:
            value = hand.cards[1].get_value()
            if value == 1:
                print_hand += ' ({} or {})'.format(value, value + 10)
            else:
                print_hand += ' ({})'.format(value)
        elif not hidden and len(hand.cards) > 1:
            if hand_type == 'soft':
                print_hand += ' ({} {} or {})'.format(
                    hand_type, value - 10, value)
            else:
                print_hand += ' ({} {})'.format(hand_type, value)
        if not hidden:
            if hand.busted:
                print_hand += ' BUSTED '
            elif hand.blackjack:
                print_hand += ' BLACKJACK! '
        return print_hand
