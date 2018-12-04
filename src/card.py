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


class PlayingCard(Card):
    suits = '♠♥♦♣'
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # nopep8
    face_cards = set()

    @property
    def is_face_card(self):
        return self.number in self.face_cards


class BlackJackCard(PlayingCard):
    face_cards = {'10', 'J', 'Q', 'K'}

    def get_value(self):
        if self.number == 'A':
            return 1
        elif self.is_face_card:
            return 10
        else:
            return int(self.number)
