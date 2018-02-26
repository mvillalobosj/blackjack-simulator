class Table:
    maximum_bet = 0
    minimum_bet = 0
    ante = 0
    deck = None

    @staticmethod
    def setup(minimum_bet, maximum_bet, ante, deck):
        Table.maximum_bet = maximum_bet
        Table.minimum_bet = minimum_bet
        Table.ante = ante
        Table.deck = deck
