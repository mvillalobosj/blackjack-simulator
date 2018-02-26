from .renderer import Renderer


class Game:
    def __init__(self, renderer=None):
        self.renderer = renderer or Renderer()

    def deal_game(self, player, dealer):
        dealer.reset()
        player.reset()

        player.add_hand()
        self.renderer.render_deal()

        dealer.add_hand()
        self.renderer.render_deal()

        player.add_card_to_hand(0, dealing=True)
        self.renderer.render_deal()

        dealer.add_card_to_hand(0, dealing=True)
        self.renderer.render_deal()

    def run_game(self, player, dealer):
        self.deal_game(player, dealer)

        self.renderer.pre_game_render()

        if not dealer.hand.blackjack:
            while player.active_hands:
                hand = player.active_hands[0]
                if hand.card_count == 1 and hand.was_split:
                    player.hit(hand)
                allowed_moves = player.allowed_moves(hand)
                if not allowed_moves:
                    continue
                move = self.get_move(hand, allowed_moves, player, dealer)

                if move not in allowed_moves:
                    raise Exception(
                        "Cannot make that move! "
                        "move: {} allowed moves: {}".format(
                            move, allowed_moves))

                player.make_move(move, hand)
                self.renderer.render_game()

        if any([not (h.busted or h.blackjack) for h in player.hands]):
            while not dealer.hand.locked:
                dealer.make_move()

        winnings = self.get_winnings(dealer, player)
        self.renderer.post_game_render(winnings)
        return winnings

    def get_winnings(self, dealer, player):
        total_winnings = 0
        dealer_hand = dealer.hands[0]
        for hand in player.hands:
            if hand.busted:
                total_winnings -= hand.bet_value
            elif hand.blackjack and not dealer_hand.blackjack:
                total_winnings += hand.bet_value * 3 / 2
            elif dealer_hand.busted:
                total_winnings += hand.bet_value
            else:
                _, hand_value = hand.hand_value
                _, dealer_value = dealer_hand.hand_value
                if hand_value > dealer_value:
                    total_winnings += hand.bet_value
                elif hand_value < dealer_value:
                    total_winnings -= hand.bet_value
        return total_winnings


class AutomaticGame(Game):
    def get_move(self, hand, allowed_moves, player, dealer):
        return player.suggested_move(hand, dealer.hand.cards[1], allowed_moves)


class InteractiveGame(Game):
    formatted_moves = {
        'h': '(h)it',
        's': '(s)tand',
        'd': '(d)ouble down',
        'p': 's(p)lit'
    }

    def __init__(self, renderer, show_hints):
        super(InteractiveGame, self).__init__(renderer)
        self.show_hints = show_hints

    def get_move(self, hand, allowed_moves, player, dealer):
        moves = [self.formatted_moves[move] for move in allowed_moves]
        print("\n\nHand {}".format(hand.hand_number))
        print("Allowed Moves: {}".format(" ".join(moves)))

        if self.show_hints:
            suggested_move = player.suggested_move(
                hand, dealer.hand.cards[1], allowed_moves)
            print("Suggested Move: {}".format(
                self.formatted_moves[suggested_move]))

        print("----")
        move = input("What's your Move?: ")
        while move not in allowed_moves:
            print("invalid selection")
            move = input("What's your Move?: ")
        return move
