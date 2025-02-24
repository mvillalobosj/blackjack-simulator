import json

from src import betting


class GameRules:

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
        12: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
        13: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
        14: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
        15: ['h', 'h', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
        16: ['h', 'h', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
        17: ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # nopep8
        18: ['d', 'd', 'd', 'd', 'd', 's', 's', 'h', 'h', 'h'],  # nopep8
        19: ['s', 's', 's', 's', 'd', 's', 's', 's', 's', 's'],  # nopep8
        20: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # nopep8
        21: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's']   # nopep8
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

    automatic_betting_systems = [
        betting.AlexSystem,
        betting.RyanSystem,
        betting.OscarSystem,
        betting.ProgressiveLosingSystem,
        betting.ProgressiveWinningSystem,
        betting.ThirteenTwentySix
    ]

    interactive_betting_systems = [
        betting.InteractiveBetter
    ]

    chip_count = 200
    winnings_goal = 200
    betting_unit = 5
    walk_away_amount = 0
    table_maximum = 500
    table_minimum = 5
    table_ante = 0
    table_deck_count = 6
    table_cut_card_position = 52

    session_count = 1000
    no_hints = False
    card_list = ()

    blackjack_modifier = 1.5

    # dealer rules
    dealer_hit_soft_17 = True

    # split rules
    resplit_maximum = 2
    no_resplit_aces = True
    no_split_aces = False
    multiple_draw_after_split_aces = False
    split_tens_must_be_same = False

    @classmethod
    def set_rules_from_json(cls, rules):
        dict_rules = json.loads(rules)
        for key, value in dict_rules.items():
            setattr(cls, key, value)
