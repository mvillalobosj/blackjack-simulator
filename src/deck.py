from copy import deepcopy
import random

from .card import BlackJackCard


class DeckEmpty(Exception):
    pass


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
            sorted_decks.extend(self.card_obj.get_all_cards())
        return sorted_decks

    def __str__(self):
        return '\n'.join(str(card) for card in self.deck)


class BlackJackDeck(Deck):
    def __init__(self, num_decks, cut_card_position):
        super(BlackJackDeck, self).__init__(BlackJackCard, num_decks)
        self.cut_card_position = cut_card_position

    def deal(self):
        if len(self.shuffled_deck) <= self.cut_card_position:
            self.shuffle()
        return super(BlackJackDeck, self).deal()


class RiggedDeck(BlackJackDeck):
    def __init__(self, rigged_cards, *args, **kwargs):
        self._rigged_cards = rigged_cards
        super().__init__(*args, **kwargs)

    def swap(self, ind1, ind2):
        deck = self.shuffled_deck
        deck[ind1], deck[ind2] = deck[ind2], deck[ind1]

    def shuffle(self):
        super(RiggedDeck, self).shuffle()
        if not self._rigged_cards:
            return
        rigged_cards = deepcopy(self._rigged_cards)
        for index, card in enumerate(self.shuffled_deck):
            for en_index, (new_card, new_index) in enumerate(rigged_cards):
                if new_card.number == card.number:
                    self.swap(index, -1 * new_index)
                    rigged_cards.pop(en_index)
