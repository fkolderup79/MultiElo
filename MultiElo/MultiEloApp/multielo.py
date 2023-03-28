import pandas as pd
import openpyxl
from .class_elo import Elo
from .class_player import Player


def calculate(s_settings, t_result, t_distr):
    # This function will calculate ELO data and return a list of all player with corresponding ELO data

    # Instantiate the ELO Class
    class_elo = instantiate_elo(s_settings, t_distr)

    # Results - Convert Data Frame to Data
    t_game, t_player = get_game_list(t_result, class_elo)

    # Do Calculations for Multi-Elo based on Games
    for s_game in t_game:
        t_player_points_init = []

        calculate_player_points(s_game, class_elo)

        # Get Players that will receive points for this Game based on Point Distribution
#        t_player_win = get_player_win(s_game["Position Table"], s_game["Count"], t_distr)

        # Calculate Points given among Players without Distribution Adjustment
#        t_player_points_init = get_player_points_init(s_game, class_elo)

        # Get Player list with adjusted percentages based on distribution
#        t_player_adj = get_player_adj(t_player_points_init, s_game["Count"], t_distr, class_elo.k)

        # Adjust Points based on adjusted percentages
#        do_player_points_adj(t_player_points_init, t_player_adj, s_game["Game ID"])

    # Refresh Player with an ELO score for every game
    points = 0
    for s_player in t_player:
        s_player["Player"].refresh_elo_game(t_game)
        for s_elo in s_player["Player"].t_elo:
            points += s_elo["Points"]

    return t_player


def instantiate_elo(s_setts, t_distr):
    # This function will instantiate the ELO Class
    class_elo = Elo(s_setts["ELO Base"], s_setts["K-factor"], s_setts["E-factor"], t_distr, s_setts["Multiplier"])
    return class_elo


def get_game_list(t_result, class_elo):
    # This function will prepare the game list based on the results with the player IDs
    # --- The list of Player IDs will be in the order of position in the game
    # --- In case of a tie would be identified by a player starting with "=="
    # --- Example: P1, P2, ==P3, ==P4, P5, P6
    # --- This would result in 1st : P1, 2nd: P2 & P3 & P4, 5th: P5 and 6th: P6
    t_game = []
    t_player = []
    for key, values in t_result.items():
        game_id = key
        count = 0
        t_player_id = []
        for v in values:
            count += 1
            if count == 1:
                date = v
            elif count == 2:
                player_count = v
            elif count == 3:
                t_distr = convert_from_distr_string(v)
            else:
                t_player_id.append({"Player ID": v})
        t_position = []
        position = 0
        for s_player_id in t_player_id:
            player_id = ''
            flag_tie = ''
            # Check for indicator for tie (which is starting with "&=")
            if s_player_id["Player ID"][0:2] == '&=':
                player_id = s_player_id["Player ID"][2:]
                flag_tie = 'X'
            else:
                player_id = s_player_id["Player ID"]
            if position == 0:
                position = 1
                position_next = 2
            else:
                if flag_tie == 'X':
                    position_next += 1
                else:
                    position = position_next
                    position_next += 1
            player = ''
            # Get Player Class - Create new Player Class if not already crated
            for s_player in t_player:
                if s_player["Player"].id == player_id:
                    player = s_player["Player"]
                    break
            if player == '':
                player = Player(player_id, class_elo)
                t_player.append({"Player": player})
            distr = 0
            for s_distr in t_distr:
                if s_distr["Position"] == position:
                    distr = s_distr["Distribution"]
                    break
            t_position.append({'Position': position, 'Player': player, 'Distribution': distr})
        t_game.append({'Game ID': game_id, 'Date': date, 'Count': player_count, 'Position Table': t_position})
    return t_game, t_player


def convert_from_distr_string(distr_string):
    t_distr = []
    distr = ''
    position = 0
    for c in distr_string:
        if c == '-':
            position += 1
            distr_float = float(distr)
            t_distr.append({"Position": position, "Distribution": distr_float})
            distr = ''
            continue
        distr = distr + c
    position += 1
    distr_float = float(distr)
    t_distr.append({"Position": position, "Distribution": distr_float})
    return t_distr


def get_player_win(t_position, player_count,  t_distr):
    # This function will return a list of Positions with Player that will receive points (based on distribution)
    t_player_win = []
    distr_count = get_distr_count(player_count, t_distr)
    for s_position in t_position:
        if s_position["Position"] <= distr_count:
            t_player_win.append({'Position': s_position["Position"], 'Player': s_position["Player"]})
        else:
            break
    return t_player_win


def get_distr_count(player_count, t_distr):
    # This function will return how many Positions will receive points based on distribution for player count
    # Example:  The distribution is [8,1,80] [8,3,40] [12,1,80] [12,2,40] [12,4,20]
    #--- If Player count is 10 then there would be up to 3 people receiving points
    #---   The reason is because 10 >= 8 and the highest position to is 3 in [8,3,40]
    distr_count = 0
    for s_distr in t_distr:
        if player_count >= s_distr["Count From"]:
             distr_count = s_distr["Position To"]
    return distr_count


def get_player_points_init(s_game, class_elo):
    # This function will return Player points without distribution adjustments
    # --- A winning Player will receive points from each Player with less or equal result position
    t_player_points_init = []
    game_id = s_game["Game ID"]

    for s_pos_win in s_game["Position Table"]:
        distr = 0
        if s_pos_win["Distribution"] > 0:
            distr = s_pos_win["Distribution"]
            player_win = s_pos_win["Player"]
            pos_win = s_pos_win["Position"]
            t_points_won = []
            for s_pos_loose in s_game["Position Table"]:
                if s_pos_loose["Player"] != s_pos_win["Player"]:
                    if s_pos_loose["Position"] >= s_pos_win["Position"]:
                        player_loose = s_pos_loose["Player"]
                        pos_loose = s_pos_loose["Position"]

                        # Calculate points that Winning Player will get from Player with less or equal result position
                        points = class_elo.calculate(player_win.get_elo(game_id), player_loose.get_elo(game_id))

                        # Collect Points given among players (without distribution adjustment)
                        t_points_won.append({'Player': player_loose, 'Position': pos_loose, 'Points': points})

            # Set Player Position and Point Table (without distribution adjustment)
            t_player_points_init.append({"Player": player_win, "Position": pos_win, "Distribution": distr, "Points Table": t_points_won})

    return t_player_points_init


def get_player_adj(t_player_points_init, player_count, t_distr, k_factor):
    # This function will calculate the percentage adjustment needed of player points for each player
    #--- The logic is to figure out how

    # Get calculated initial distribution (based on equal rating and taking ties into consideration)
    t_player_distr_init = get_player_distr_init(t_player_points_init, player_count, t_distr)

    # Collect Actual Points and Initial Points
    t_player_points_calc_init = []
    calc_points_total = 0
    for s_player_points_won in t_player_points_init:
        player = s_player_points_won["Player"]
        distr = s_player_points_won["Distribution"]
        points = 0
        calc_points = 0
        for s_points_won in s_player_points_won["Points Table"]:
            points += s_points_won["Points"]
            calc_points += 1 * k_factor / 2
            calc_points_total += 1 * k_factor / 2
        for s_player_points_lost in t_player_points_init:
            if s_player_points_lost["Player"] != s_player_points_won["Player"]:
                for s_points_lost in s_player_points_lost["Points Table"]:
                    if s_points_lost["Player"] == s_player_points_won["Player"]:
                        points -= s_points_lost["Points"]
                        calc_points -= 1 * k_factor / 2
                        calc_points_total -= 1 * k_factor / 2
        t_player_points_calc_init.append({'Player': player, 'Position': s_player_points_won["Position"], 'Distribution': distr, 'Points': points, 'Calc Points': calc_points})

    t_player_points_calc_adj = []
    points_calc_remaining = 0
    s_player_points_zero = ''
    for s_player_points_calc_init in t_player_points_calc_init:
        if s_player_points_calc_init["Calc Points"] != 0:
            points_calc_adj = ( calc_points_total * ( s_player_points_calc_init["Distribution"] / 100 ) ) - s_player_points_calc_init["Calc Points"]
            points_calc_remaining -= points_calc_adj
            t_player_points_calc_adj.append(
                {'Player': s_player_points_calc_init["Player"], 'Position': s_player_points_calc_init["Position"], 'Points': s_player_points_calc_init["Points"],
                 'Calc Points': s_player_points_calc_init["Calc Points"], 'Adj Points': points_calc_adj})
        elif s_player_points_calc_init["Distribution"] != 0:
            s_player_points_zero = s_player_points_calc_init

    if s_player_points_zero != '':
        t_player_points_calc_adj.append(
            {'Player': s_player_points_zero["Player"], 'Position': s_player_points_zero["Position"], 'Points': s_player_points_zero["Points"],
            'Calc Points': s_player_points_zero["Calc Points"], 'Adj Points': points_calc_remaining})

    t_player_adj = []
    points_adj_total = 0
    for s in t_player_points_calc_adj:
        points_adj = ( s["Adj Points"] + points_adj_total ) / (player_count - s["Position"])
        points_adj_total += points_adj
        t_player_adj.append({'Player': s["Player"], 'Adj Points': points_adj})

    return t_player_adj


def get_player_distr_init(t_player_points, player_count, t_distr):
    t_player_distr_init = []
    for s_player_points_won in t_player_points:
        distr = s_player_points_won["Distribution"]
        position = s_player_points_won["Position"]
        position_count = 1
        for s_player_points_lost in t_player_points:
            if s_player_points_lost["Player"] != s_player_points_won["Player"]:
                if s_player_points_lost["Position"] == s_player_points_won["Position"]:
                    position += 1
                    position_count += 1
                    distr += s_player_points_lost["Distribution"]
        distr_init = distr / position_count
        t_player_distr_init.append({'Player': s_player_points_won["Player"], 'Distribution': distr_init})
    return t_player_distr_init


def get_game_points_total(player_count, t_distr, k_factor):
    # This function will return the total points given in this game based on player count, the number of players
    # receiving points (based on distribution) and the K-Factor on the ELO calculation
    #--- Example for a 6 player game if 2 player receive points based on distribution [3,1,70] [3,2,30] and K-factor = 10
    #------ Then 1st player will receive 5 points from 5 players = 25 points
    #------ Then 2nd player will receive 5 points from 4 players and give away 5 points to 1st player = 15 points
    #------ So total game points is 40 points = 25 points player 1 and 15 points player 2
    game_points_total = 0
    count = 0
    count_factor = 0
    distr_count = get_distr_count(player_count, t_distr)
    # Calculate total points for all positions receiving points
    while count < distr_count:
        game_points_total += (player_count - count_factor) * (k_factor / 2)
        count += 1
        count_factor += 2
    return game_points_total


def get_player_points_total(s_player_points, t_player_points):
    player_points_total = 0
    # First Add up Points won by Player
    for s_points_won in s_player_points["Points_table"]:
        player_points_total += s_points_won["Points"]
    # Second Subtract Points lost to other Players
    for s_player_points_other in t_player_points:
        if s_player_points_other["Player ID"] != s_player_points["Player ID"]:
            for s_points_won in s_player_points_other["Points Table"]:
                if s_points_won["Player ID"] == s_player_points["Player ID"]:
                    player_points_total -= s_points_won["Points"]
    return player_points_total


def get_adjust_percentage(player_points, player_position, player_count, t_distr, k_factor):
    # This Function will get the percentage difference for the calculated player points without distribution
    # vs with distribution (based on that all players have an equal rating)
    #--- Example 6 players (all same rating), Top 2 get points with the distribution 1st place 70% & 2nd place 30%
    #------ Without distribution (K-factor = 10) - 1st will get 25 points (62.5%) and 2nd will get 15 points (37.5%)
    #------ That means 1st place would calculate an adjust percentage of 12% = (70 - 62.5) / 62.5
    #------ That means 2nd place would calculate an adjust percentage of -20% = (30 - 37.5) / 37.5
    distr_count = get_distr_count
    count = 0
    count_factor = 0
    total_points = 0
    # Calculate total points for all positions receiving points
    while count < distr_count:
        total_points = total_points + (player_count - count_factor) * (k_factor / 2)
        count += 1
        count_factor += 2
    # Get distribution percentage based on player count and position
    distr_percentage = get_distr_percentage(player_count, player_position, t_distr)
    # Calculate adjust percentage
    adjust_percentage = ((distr_percentage/100) - (player_points / total_points)) / (player_points / total_points)
    return adjust_percentage


def get_distr_count(player_count, t_distr):
    # This function will return the number of positions that will receive points based on the distribution count
    distr_count = ''
    for s_distr in t_distr:
        if player_count >= s_distr["Count From"]:
            distr_count = s_distr["Position To"]
        else:
            break
    return distr_count


def get_distr_percentage(player_count, player_position, t_distr):
    # This function will return the distribution percentage based on player count and player_position
    #--- Example distribution for 10 players [8,1,80] [8,3,40] [12,1,80] [12,2,40] [12,4,20]
    #--- That means 1st should get 80, 2nd should get 40 and 3rd should get 40 (it would use count from 8)
    #--- 1st place distribution percentage 50% = 80 / (80 + 40 + 40)
    #--- 2nd and 3rd place distribution percentage 25% = 40 / (80 + 40 + 40)
    distr_from = 0
    for s_distr in t_distr:
        if player_count < s_distr["Count From"]:
            # Exit if Count From is higher than player count (this table is sorted)
            #--- That means use distribution and distribution total found for previous Count From
            break
        if distr_from != s_distr["Count From"]:
            # Clear distribution and distribution total for new valid Count From
            distr = 0
            distr_total = 0
        if player_position >= s_distr["Position To"]:
            # New valid distribution found for player position
            distr = s_distr["Distribution"]
        distr_total += s_distr["Distribution"]
        distr_from = s_distr["Count From"]

    if distr_total > 0:
        distr_percentage = distr / distr_total
    return distr_percentage


def do_player_points_adj(t_player_points_init, t_player_adj, game_id):
    for s_player_points_init in t_player_points_init:
        player_win = s_player_points_init["Player"]
        for s_player_adj in t_player_adj:
            if s_player_adj["Player"] == s_player_points_init["Player"]:
                break
        for s_points_won in s_player_points_init["Points Table"]:
            player_loose = s_points_won["Player"]
            points = s_points_won["Points"] + (s_player_adj["Adj Points"])
            player_win.t_elo.append({"Game ID": game_id, "Player": player_loose, "Points": points})
            player_loose.t_elo.append({"Game ID": game_id, "Player": player_win, "Points": points / -1})


def calculate_player_points(s_game, class_elo):
    # This function will return Player points without distribution adjustments
    # --- A winning Player will receive points from each Player with less or equal result position
    t_player_points_init = []
    game_id = s_game["Game ID"]

    for s_pos_win in s_game["Position Table"]:
        distr = 0
        if s_pos_win["Distribution"] > 0:
            distr_win = s_pos_win["Distribution"]
            player_win = s_pos_win["Player"]
            pos_win = s_pos_win["Position"]
            t_points_won = []
            for s_pos_loose in s_game["Position Table"]:
                if s_pos_loose["Player"] != s_pos_win["Player"]:
                    if s_pos_loose["Position"] >= s_pos_win["Position"]:
                        player_loose = s_pos_loose["Player"]
                        pos_loose = s_pos_loose["Position"]
                        distr_loose = s_pos_loose["Position"]

                        # Calculate points that Winning Player will get from Player with less or equal result position
                        points = class_elo.calculate(player_win.get_elo(game_id), player_loose.get_elo(game_id))
                        points = points * ( distr_win - distr_loose ) / 100.

                        player_win.t_elo.append({"Game ID": game_id, "Player": player_loose, "Points": points})
                        player_loose.t_elo.append({"Game ID": game_id, "Player": player_win, "Points": points / -1})
