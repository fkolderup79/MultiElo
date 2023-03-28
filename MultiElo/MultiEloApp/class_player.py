from datetime import datetime


class Player:

    def __init__(self, id, class_elo):
        self.id = id
        self.class_elo = class_elo
        self.elo = class_elo.base
        self.t_elo = []
        self.t_elo_game = []
        self.game_count = 0
        self.elo_average = 0

    def get_elo(self, game_id):
        elo = self.class_elo.base
        for s_elo in self.t_elo:
            if s_elo["Game ID"] <= game_id:
                elo += s_elo["Points"]
        return elo

    def calculate(self, game_id, player_loss, pos_win, pos_loss):
        last_game_id = game_id - 1
        points = self.class_elo.calculate(player_loss.get_elo(last_game_id), self.get_elo(last_game_id))
        self.t_elo.append({'Game ID': game_id, 'Player ID': player_loss.id, 'Position': pos_win, 'Points': points})
        player_loss.t_elo.append({'Game ID': game_id, 'Player ID': self.id, 'Position': pos_loss, 'Points': points/-1})

    def refresh_elo_game(self, t_game):
        t_elo_game = []
        self.game_count = 0
        elo_total = 0
        date = datetime.min
        date = date.date()
        self.t_elo_game.append({'Game ID': 0, 'Date': date, 'Count': 0, 'Position': 0, 'ELO': self.class_elo.base})
        for s_game in t_game:
            game_id = s_game["Game ID"]
            date = s_game["Date"]
            count = s_game["Count"]
            self.elo = round(self.class_elo.base + (self.get_elo(game_id) - self.class_elo.base) * self.class_elo.m)
            pos = 0
            for s_pos in s_game["Position Table"]:
                if s_pos["Player"] == self:
                    pos = s_pos["Position"]
            self.t_elo_game.append({'Game ID': game_id, 'Date': date, 'Count': count,'Position': pos, 'ELO': self.elo})
            found = ''
            for s_elo in self.t_elo:
                if s_elo["Game ID"] == game_id:
                    found = 'X'
            if found == 'X':
                self.game_count += 1
                elo_total += self.elo
        self.elo_average = round(elo_total / self.game_count)