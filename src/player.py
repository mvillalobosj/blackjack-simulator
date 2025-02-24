from .rules import GameRules
from .table import Table

SOFT = 'soft'
HARD = 'hard'
PAIR = 'pair'
BLACKJACK = 'blackjack'


HIT = 'h'
STAND = 's'
SPLIT = 'p'
DOUBLE_DOWN = 'd'


class Hand:
    def __init__(self, cards, hand_number, bet_value=0):
        self.cards = cards
        self._locked = False
        self._additional_cards = 0
        self._busted = False
        self._double_down = False
        self._blackjack = False
        self._was_split = False
        self.hand_number = hand_number
        self.calculate_value()
        self.bet_value = bet_value

    def reset_additional_cards(self):
        self._additional_cards = 0

    @property
    def hand_value(self):
        return self._hand_value

    @property
    def card_count(self):
        return len(self.cards)

    def calculate_value(self):
        self._busted = False
        hand_type = HARD

        if self.is_blackjack():
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

    @property
    def was_split(self):
        return self._was_split

    @was_split.setter
    def was_split(self, value):
        self._was_split = value

    def add_card(self, card, dealing=False):
        if not dealing:
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

    def is_pair(self):
        if self.added_cards > 0 or len(self.cards) != 2:
            return False
        return (
            self.cards[0].number == self.cards[1].number or
            (self.cards[0].is_face_card and self.cards[1].is_face_card and not GameRules.split_tens_must_be_same)
        )

    def is_blackjack(self):
        if self.added_cards > 0 or len(self.cards) != 2:
            return False
        return ((self.cards[0].is_face_card and self.cards[1].number == 'A') or
                (self.cards[1].is_face_card and self.cards[0].number == 'A'))

    @staticmethod
    def _get_value(cards):
        value = 0
        has_ace = False
        for card in cards:
            value += card.get_value()
            if card.number == 'A':
                has_ace = True
        return (has_ace, value)

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)


class Character:
    def __init__(self):
        self.hands = []
        self.move_map = {
            HIT: self.hit,
            STAND: self.stand,
            SPLIT: self.split,
            DOUBLE_DOWN: self.double_down
        }
        self.moves = []

    def reset(self):
        self.hands = []
        self.moves = []

    def make_move(self, move, hand):
        self.moves.append(move)
        self.move_map[move](hand)

    def hit(self, hand):
        hand.add_card(Table.deck.deal())

    def stand(self, hand):
        hand.lock()

    def split(self, hand):
        new_hand = self.add_hand([hand.remove_card()])
        hand.was_split = True
        new_hand.was_split = True

    def make_bet(self):
        return 0

    def double_down(self, hand):
        self.hit(hand)
        hand.lock()
        hand.double_down = True
        hand.bet_value += self.current_bet
        self.make_bet()

    def add_hand(self, cards=None):
        cards = cards or [Table.deck.deal()]
        new_hand = Hand(cards, len(self.hands) + 1, self.make_bet())
        self.hands.append(new_hand)
        new_hand.reset_additional_cards()
        return new_hand

    def add_card_to_hand(self, hand_number, *args, **kwargs):
        self.hands[hand_number].add_card(Table.deck.deal(), *args, **kwargs)

    @property
    def active_hands(self):
        return [hand for hand in self.hands if not hand.locked]


class Dealer(Character):
    def allowed_move(self):
        if self.hand.locked:
            return None

        hand_type, value = self.hand.hand_value
        if value < 17 or (value == 17 and hand_type == SOFT and GameRules.dealer_hit_soft_17):
            return HIT
        else:
            return STAND

    def make_move(self):
        super().make_move(self.allowed_move(), self.hand)

    @property
    def hand(self):
        if not self.hands:
            return None
        return self.hands[0]

    def __str__(self):
        if self.hands:
            return str(self.hands[0])
        else:
            return ''


class Player(Character):

    def can_split(self, hand):
        if not hand.is_pair():
            return False
        if GameRules.resplit_maximum > 0 and len(self.hands) > GameRules.resplit_maximum:
            return False
        if hand.cards[0].number == 'A':
            if GameRules.no_split_aces:
                return False
            if GameRules.no_resplit_aces and hand.was_split:
                return False

        return True

    def allowed_moves(self, hand):
        hand_type, value = hand.hand_value
        if hand.busted or hand.locked:
            return set()

        allowed_moves = set([HIT, STAND])

        if (
            hand.was_split and
            hand.cards[0].number == 'A' and
            len(hand.cards) > 1 and
            not GameRules.multiple_draw_after_split_aces
        ):
            allowed_moves.remove(HIT)

        if self.can_split(hand):
            allowed_moves.add(SPLIT)

        if hand.added_cards == 0 and HIT in allowed_moves:
            allowed_moves.add(DOUBLE_DOWN)

        return allowed_moves

    def suggested_move(self, hand, dealer_card, allowed_moves):
        hand_type, value = hand.hand_value
        dealer_index = 0
        if dealer_card.number == 'A':
            dealer_index = 9
        elif dealer_card.is_face_card:
            dealer_index = 8
        else:
            dealer_index = int(dealer_card.number) - 2

        if SPLIT in allowed_moves:
            suggested_move = GameRules.pair_moves[value][dealer_index]
        elif hand_type == HARD:
            suggested_move = GameRules.hard_moves[value][dealer_index]
        elif hand_type == SOFT:
            suggested_move = GameRules.soft_moves[value][dealer_index]

        if suggested_move == DOUBLE_DOWN and DOUBLE_DOWN not in allowed_moves:
            suggested_move = HIT
        if suggested_move == HIT and HIT not in allowed_moves:
            suggested_move = STAND

        return suggested_move


class Gambler(Player):
    def __init__(self, base_chip_count, winnings_goal, bet_unit, walk_away=0):
        super().__init__()

        self.base_chip_count = base_chip_count
        self.walk_away = walk_away
        self.goal = base_chip_count + winnings_goal

        self.current_chip_count = base_chip_count
        self.bet_unit = bet_unit
        self.current_bet = bet_unit
        self.previous_game_winnings = 0
        self.total_bet = 0

    def reset_chip_count(self):
        self.current_chip_count = self.base_chip_count
        self.current_bet = self.bet_unit

    def reset(self):
        super().reset()
        self.total_bet = 0

    def can_play(self, minimum_bet):
        return (
            self.goal >
            self.current_chip_count >
            max(self.walk_away, minimum_bet)
        )

    @property
    def current_bet(self):
        return self._current_bet

    @current_bet.setter
    def current_bet(self, value):
        self._current_bet = value

    def remove_chips(self, value=None):
        if value is None:
            value = self.current_bet
        self.current_chip_count -= value
        return value

    def allowed_moves(self, hand):
        allowed_moves = super().allowed_moves(hand)

        if self.current_chip_count - self.current_bet < 0:
            allowed_moves.discard(SPLIT)
            allowed_moves.discard(DOUBLE_DOWN)

        return allowed_moves

    def collect_winnings(self, winnings):
        net_winnings = winnings + self.total_bet
        self.current_chip_count += net_winnings
        self.previous_game_winnings = winnings

    def make_initial_bet(self, betting_system):
        next_bet = betting_system.get_next_bet(
            self.previous_game_winnings,
            self.current_bet,
            self.bet_unit)

        self.current_bet = max(
            min(next_bet, self.current_chip_count, Table.maximum_bet),
            Table.minimum_bet)

    def make_bet(self):
        self.total_bet += self.current_bet
        return self.remove_chips()
