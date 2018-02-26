from copy import deepcopy
import random


class DeckEmpty(Exception):
    pass


class Card:
    suits = []
    numbers = []

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def get_value(self):
        pass

    @classmethod
    def get_all_cards(cls):
        return [
            cls(suit, number) for suit in cls.suits for number in cls.numbers
        ]

    def __str__(self):
        return "{}{}".format(self.number, self.suit)


class Deck:
    def __init__(self, card_obj, num_decks=1):
        self.card_obj = card_obj
        self.base_deck = self._get_sorted_deck(num_decks)
        self.shuffled_deck = []

    def shuffle(self):
        shuffled_deck = deepcopy(self.base_deck)

        for i in range(len(shuffled_deck) - 1):
            swap_position = random.randint(i, len(shuffled_deck) - 1)
            shuffled_deck[swap_position], shuffled_deck[i] =\
                shuffled_deck[i], shuffled_deck[swap_position]

        self.shuffled_deck = shuffled_deck

    def deal(self):
        return deepcopy(self.shuffled_deck.pop())

    def _get_sorted_deck(self, num_decks):
        sorted_decks = []
        for number in range(num_decks):
            for card in self.card_obj.get_all_cards():
                sorted_decks.append(card)
        return sorted_decks

    def __str__(self):
        return '\n'.join(str(card) for card in self.deck)


class PlayingCard(Card):
    suits = '♠♥♦♣'
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # nopep8
    face_cards = ['10', 'J', 'Q', 'K']

    @property
    def is_face_card(self):
        return self.number in self.face_cards


class BlackJackCard(PlayingCard):

    def get_value(self):
        if self.number == 'A':
            return 1
        elif self.is_face_card:
            return 10
        else:
            return int(self.number)


class BlackJackDeck(Deck):
    def __init__(self, num_decks, cut_card_position):
        super(BlackJackDeck, self).__init__(BlackJackCard, num_decks)
        self.cut_card_position = cut_card_position

    def deal(self):
        if len(self.shuffled_deck) <= self.cut_card_position:
            self.shuffle()
        return super(BlackJackDeck, self).deal()


class RiggedDeck(BlackJackDeck):
    def swap(self, ind1, ind2):
        deck = self.shuffled_deck
        deck[ind1], deck[ind2] = deck[ind2], deck[ind1]

    def shuffle(self, cards):
        super(RiggedDeck, self).shuffle()
        for index, card in enumerate(self.shuffled_deck):
            if not cards:
                return
            for en_index, (new_card, new_index) in enumerate(cards):
                if new_card.number == card.number:
                    self.swap(index, -1 * new_index)
                    cards.pop(en_index)
