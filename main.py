import argparse
import json

from tqdm import tqdm

from src.analytics import Reporter
from src.card import BlackJackCard
from src.deck import RiggedDeck
from src.game import AutomaticGame, InteractiveGame
from src.player import Dealer, Gambler
from src.renderer import InteractiveRenderer
from src.rules import GameRules
from src.table import Table


def start(is_automatic, json_rules):
    GameRules.set_rules_from_json(json_rules)
    shuffle_each_game = False
    card_list = []
    if GameRules.card_list:
        for i, card in enumerate(GameRules.card_list, 1):
            if card != 'X':
                card_list.append((BlackJackCard('', card), i))
        shuffle_each_game = True

    deck = RiggedDeck(
        rigged_cards=card_list,
        num_decks=GameRules.table_deck_count,
        cut_card_position=GameRules.table_cut_card_position)

    gambler = Gambler(
        base_chip_count=GameRules.chip_count,
        winnings_goal=GameRules.winnings_goal,
        bet_unit=GameRules.betting_unit,
        walk_away=GameRules.walk_away_amount)
    Table.setup(
        maximum_bet=GameRules.table_maximum,
        minimum_bet=GameRules.table_minimum,
        ante=GameRules.table_ante,
        deck=deck
    )
    dealer = Dealer()

    if is_automatic:
        betting_systems = GameRules.automatic_betting_systems
        game = AutomaticGame()
        print_progress = True
    else:
        betting_systems = GameRules.interactive_betting_systems
        game = InteractiveGame(
            InteractiveRenderer(gambler, dealer), not GameRules.no_hints)
        print_progress = False

    run_game(betting_systems, game, dealer, gambler, shuffle_each_game, print_progress)


def run_game(betting_systems, game, dealer, gambler, shuffle_each_game, print_progress):
    winning_amounts = []
    for system in betting_systems:
        better = system(gambler, Table)
        system_name = better.__class__.__name__

        reporter = Reporter(system_name, gambler, Table)
        reporter.reset_overall_report()

        reporter.reset_bet_report(gambler.bet_unit)

        range_func = range(GameRules.session_count)
        if print_progress:
            range_func = tqdm(
                range(GameRules.session_count),
                desc=system_name,
                unit='sessions')
        for i in range_func:
            reporter.reset_session()
            better.reset()
            gambler.reset_chip_count()
            winnings = 0
            while gambler.can_play(Table.minimum_bet + Table.ante):
                if shuffle_each_game:
                    Table.deck.shuffle()

                gambler.remove_chips(Table.ante)

                gambler.make_initial_bet(better)

                winnings = game.run_game(gambler, dealer)

                gambler.collect_winnings(winnings)

                reporter.record_game_results()

            if gambler.current_chip_count < 0:
                print(gambler.current_chip_count)
                raise Exception("something wrong with betting")
            reporter.record_session_results()

        reporter.record_bet_results()
        # reporter.print_bet_report()
        reporter.print_overall_report()
        net_earn = reporter.total_winnings - reporter.total_loss
        winning_amounts.append((system_name, net_earn))

    print("Betting Strategy Rankings")
    winning_amounts.sort(key=lambda x: x[1], reverse=True)
    for i, strategy in enumerate(winning_amounts, 1):
        print(f"{i}. {strategy[0]:<25}   {strategy[1]:>10.2f}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--automatic',
        action='store_true',
        help="Automatic Mode. If set, will play game automatically.")
    parser.add_argument(
        '-c',
        '--chip-count',
        type=int,
        default=200,
        help="Starting chip count (Default: 200)")
    parser.add_argument(
        '-g',
        '--goal',
        type=int,
        default=100,
        help="Winnings Goal (Default: 100)")
    parser.add_argument(
        '-b',
        '--bet',
        type=int,
        default=5,
        help="Betting unit (Default: 5)")
    parser.add_argument(
        '-w',
        '--walk-away',
        type=int,
        default=100,
        help="Walk Away amount (Default: 100)")
    parser.add_argument(
        '-s',
        '--session-count',
        type=int,
        default=10000,
        help="Number of sessions to play per betting strategy (Default: 10000)")
    parser.add_argument(
        '-t',
        '--table-maximum',
        type=int,
        default=500,
        help="Table maximum bet (Default: 500)")
    parser.add_argument(
        '-m',
        '--table-minimum',
        type=int,
        default=5,
        help="Table maximum bet (Default: 5)")
    parser.add_argument(
        '-e',
        '--table-ante',
        type=int,
        default=0,
        help="Ante for table (Default: 0)")
    parser.add_argument(
        '-d',
        '--deck-count',
        type=int,
        default=4,
        help="Number of decks to play (Default: 4)")
    parser.add_argument(
        '-u',
        '--cut-card-position',
        type=int,
        default=52,
        help="Position of cut card from bottom of deck (Default: 52)")
    parser.add_argument(
        '-n',
        '--no-hints',
        action='store_true',
        help="Hide hints. If set, the recommended move is not shown.")
    parser.add_argument(
        '-r',
        '--rigged',
        nargs='*',
        help='Run rigged game. Enter in the first cards in the deck. Type X to skip a position')

    args = parser.parse_args()

    card_list = args.rigged
    shuffle_each_game = False

    json_rules = json.dumps(dict(
        chip_count=args.chip_count,
        winnings_goal=args.goal,
        betting_unit=args.bet,
        walk_away_amount=args.walk_away,
        table_maximum=args.table_maximum,
        table_minimum=args.table_minimum,
        table_ante=args.table_ante,
        table_deck_count=args.deck_count,
        table_cut_card_position=args.cut_card_position,
        session_count=args.session_count,
        no_hints=args.no_hints,
        card_list=card_list
    ))
    start(args.automatic, json_rules)
