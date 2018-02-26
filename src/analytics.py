def average(l):
    if len(l) == 0:
        return 0
    return sum(l) / len(l)


class Reporter:
    def __init__(self, system_name, gambler, table):
        self.system_name = system_name
        self.reset_overall_report()
        self.gambler = gambler
        self.table = table

    def reset_overall_report(self):
        self.total_game_count = 0
        self.win_count = 0
        self.lose_count = 0
        self.reset_bet_report(0)
        self.bet_summary = []
        self.total_winnings = 0
        self.total_loss = 0

    def reset_bet_report(self, bet):
        self.bet_game_count = 0
        self.bet = bet
        self.game_count = 0
        self.bankrupt = 0
        self.hit_goal = 0
        self.hit_maximum_bet = 0
        self.max_chip_count = 0
        self.games_to_goal = []
        self.games_to_bankrupt = []
        self.winnings = []
        self.total_winnings = 0
        self.total_loss = 0

    def print_bet_report(self):
        print("Bet: {}".format(self.bet))
        print("Bankrupt Count: {}".format(self.bankrupt))
        print("Average games to bankrupt: {}".format(average(self.games_to_bankrupt)))
        print("Goal Count: {}".format(self.hit_goal))
        print("Average games to goal: {}".format(average(self.games_to_goal)))
        print("Average Winnings: {}".format(average(self.winnings)))
        print("Game Count: {}".format(self.bet_game_count))
        print("Hit Maximum Bet: {}".format(self.hit_maximum_bet))
        print("Maximum Chip Count: {}".format(self.max_chip_count))
        print("-----------------------------")

    def print_overall_report(self):
        most_goals = 0
        best_summary = {}
        for summary in self.bet_summary:
            if summary['goal_percent'] > most_goals:
                best_summary = summary
                most_goals = summary['goal_percent']

        print("System: {}".format(self.system_name))
        print("Best Bet: {}".format(best_summary['bet']))
        print("Goal Percentage: {}".format(best_summary['goal_percent']))
        print("Avg Games to Goal: {}".format(best_summary['games_to_goal']))
        print("Avg Winnings: {}".format(best_summary['average_winnings']))
        print("Total Game Count: {}".format(self.total_game_count))
        print("Win Count: {}".format(self.win_count))
        print("Lose Count: {}".format(self.lose_count))
        print("Win Percentage: {}".format(self.win_count / (self.win_count + self.lose_count)))
        print("Total Winnings: {}".format(self.total_winnings))
        print("Total Loss: {}".format(self.total_loss))
        print("Net Earnings: {}".format(self.total_winnings - self.total_loss))
        print("-----------------------------")

    def record_game_results(self):
        chip_count = self.gambler.current_chip_count
        is_max_bet = (self.gambler.current_bet == self.table.maximum_bet)
        winnings = self.gambler.previous_game_winnings

        self.max_chip_count = max(self.max_chip_count, chip_count)
        if winnings > 0:
            self.win_count += 1
            self.winnings.append(winnings)
        elif winnings < 0:
            self.lose_count += 1
        if is_max_bet:
            self.hit_maximum_bet += 1
        self.game_count += 1

    def record_session_results(self):
        chip_count = self.gambler.current_chip_count
        if chip_count >= self.gambler.goal:
            self.hit_goal += 1
            self.games_to_goal.append(self.game_count)
            self.total_winnings += chip_count - self.gambler.base_chip_count
        else:
            self.bankrupt += 1
            self.games_to_bankrupt.append(self.game_count)
            self.total_loss += self.gambler.base_chip_count - chip_count
        self.bet_game_count += self.game_count

    def record_bet_results(self):
        bet_summary = {
            'bet': self.bet,
            'goal_percent': (self.hit_goal / (self.hit_goal + self.bankrupt)) * 100,
            'games_to_goal': average(self.games_to_goal),
            'average_winnings': average(self.winnings)
        }
        self.bet_summary.append(bet_summary)

    def reset_session(self):
        self.total_game_count += self.game_count
        self.game_count = 0
