import argparse

from src import betting
from src.analytics import Reporter
from src.deck import BlackJackDeck  # , RiggedDeck, PlayingCard
from src.game import AutomaticGame, InteractiveGame
from src.player import Dealer, Gambler
from src.renderer import InteractiveRenderer
from src.table import Table


def run_game(betting_systems, game, dealer, gambler, session_count):
    for system in betting_systems:
        better = system(gambler, Table)
        reporter = Reporter(better.__class__.__name__, gambler, Table)
        reporter.reset_overall_report()

        reporter.reset_bet_report(gambler.bet_unit)

        for i in range(session_count):
            reporter.reset_session()
            better.reset()
            gambler.reset_chip_count()
            winnings = 0
            while gambler.can_play(Table.minimum_bet + Table.ante):
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


# def run_rigged_game(
#        betting_systems, game, dealer, gambler, session_count, cards):
#    for system in betting_systems:
#        better = system(gambler, Table)
#        for i in range(session_count):
#            better.reset()
#            gambler.reset_chip_count()
#            Table.deck.shuffle(cards)
#            winnings = game.run_game(gambler, dealer)

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
        default=0,
        help="Walk Away amount (Default: 0)")
    parser.add_argument(
        '-s',
        '--session-count',
        type=int,
        default=1000,
        help="Number of sessions to play per betting strategy (Default: 1000)")
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

    args = parser.parse_args()

    gambler = Gambler(
        base_chip_count=args.chip_count,
        winnings_goal=args.goal,
        bet_unit=args.bet,
        walk_away=args.walk_away)
    Table.setup(
        maximum_bet=args.table_maximum,
        minimum_bet=args.table_minimum,
        ante=args.table_ante,
        deck=BlackJackDeck(
            num_decks=args.deck_count,
            cut_card_position=args.cut_card_position
        )
    )
    dealer = Dealer()

#    Table.deck = RiggedDeck(
#        num_decks=args.deck_count,
#        cut_card_position=args.cut_card_position)
#    cards = [
#        (PlayingCard('', '2'), 1),
#        (PlayingCard('', 'J'), 3)
#    ]

    if args.automatic:
        betting_systems = [
            betting.AlexSystem,
            betting.RyanSystem,
            betting.OscarSystem,
            betting.ProgressiveLosingSystem,
            betting.ProgressiveWinningSystem,
            betting.ThirteenTwentySix
        ]
        game = AutomaticGame()
        run_game(betting_systems, game, dealer, gambler, args.session_count)
    else:
        betting_systems = [betting.InteractiveBetter]
        game = InteractiveGame(
            InteractiveRenderer(gambler, dealer),
            not args.no_hints)
        run_game(betting_systems, game, dealer, gambler, 1)
