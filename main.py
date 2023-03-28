from MultiElo.MultiEloApp.calc import calculate


t_player_class = calculate(r'C:\Users\FrederikKolderup\Downloads\Poker results python simple (5).xlsx')


t_player_points_init = []
t_player_points_init.append({'Player ID': "Player 1", 'Points': 24})
t_player_points_init.append({'Player ID': "Player 2", 'Points': 7})
t_player_adj = []
player1_perct = 5 / 100
t_player_adj.append({'Player ID': "Player 1", 'Adjust Percentage': player1_perct})
player2_perct = 0 - 10 / 100
t_player_adj.append({'Player ID': "Player 2", 'Adjust Percentage': player2_perct})
total = 31
perct_diff = 100
threshold = 1/10000

while abs(perct_diff) > threshold:
    total_calc = 0
    t_player_points_calc = []
    for s_player_adj in t_player_adj:
        for s_player_points_init in t_player_points_init:
            if s_player_points_init["Player ID"] == s_player_adj["Player ID"]:
                player_calc = s_player_points_init["Points"] * (1 + s_player_adj["Adjust Percentage"])
        total_calc += player_calc
        t_player_points_calc.append({'Player ID': s_player_adj["Player ID"], 'Points': player_calc})

    perct_diff = ((total - total_calc ) / total)

    t_player_adj_new = []
    for s_player_points_calc in t_player_points_calc:
        for s_player_adj in t_player_adj:
            if s_player_adj["Player ID"] == s_player_points_calc["Player ID"]:
                player_perct = s_player_adj["Adjust Percentage"] + (abs(s_player_adj["Adjust Percentage"]) * perct_diff)
                t_player_adj_new.append({'Player ID': s_player_adj["Player ID"], 'Adjust Percentage': player_perct})
    t_player_adj = t_player_adj_new

a = 0





player1 = 24
player2 = 7
player1_perct = 5 / 100
player2_perct = 0 - 10 / 100
total = player1 + player2


while abs(perct_diff) > threshold:
    player1_calc = player1 * ( 1 + player1_perct )
    player2_calc = player2 * ( 1 + player2_perct )
    total_calc = player1_calc + player2_calc

    perct_diff = ((total - total_calc ) / total)

    player1_perct = player1_perct + (abs(player1_perct) * perct_diff)
    player2_perct = player2_perct + (abs(player2_perct) * perct_diff)


player1_calc = player1 * (1 + player1_perct)
player2_calc = player2 * (1 + player2_perct)

total_remaining = total - (player1_calc + player2_calc)

player1_calc = player1_calc + ( total_remaining * 70 / 100)
player2_calc = player2_calc + ( total_remaining * 30 / 100)

total_calc = player1_calc + player2_calc

player1_perct = ( player1_calc / player1 ) - 1
player2_perct = ( player2_calc / player2 ) - 1

player1_calc = 24 * (1 + player1_perct)
player2_calc = 7 * (1 + player2_perct)

total_calc = player1_calc + player2_calc

a = 0




