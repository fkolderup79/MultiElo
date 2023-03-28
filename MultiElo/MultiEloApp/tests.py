#from MultiElo.MultiEloApp.calc import calculate
from data_excel import calc_excel
#from data_static import calc_static
from html_main import get_table_data
from html_main import get_graph_data
from html_main import get_table
from html_main import get_graph
from html_main import get_graph_count
from html_main import get_table_player_data
from html_main import get_table_player
from datetime import datetime
from .class_elo import Elo

player_1 = 940
player_2 = 1250

class_elo = Elo(1000, 10, 400, '', '')
points = class_elo.calculate(player_1, player_2)


datestring = 'datetime.date(2020, 4, 5)'
count = 0
date = ''
for d in datestring:
    count += 1
    if 15 <= count <= 18:
        date = date + d
    if count == 18:
        date = date + '-'
    if 20 <= count <= 21:
        if d != ' ':
            date = date + d
        else:
            date = date + '0'
    if count == 21:
        date = date + '-'
    if 23 <= count <= 24:
        if d != ' ':
            date = date + d
        else:
            date = date + '0'

date = datetime.strptime(date, "%Y-%m-%d")
date = date.date()

#t_player_class = calc_static()
#t_player_class, t_result = calc_excel(r'C:\Users\FrederikKolderup\Downloads\Poker results python simple (12).xlsx')

table_data = get_table_data(t_player_class)
table_player_data = get_table_player_data(t_player_class)
key_list = ["1", "2", "3", "4", "5", "6", "7", "8"]
table_player = get_table_player(table_player_data, key_list)

table = []
for s_result in t_result:
    table_values = []
    table_values.append(s_result["Date"])
    table_values.append(s_result["Count"])
    for s_player_id in s_result["Player ID Table"]:
        table_values.append(s_player_id["Player ID"])
    if s_result["Game ID"] == 1:
        table = {s_result["Game ID"]: table_values}
    else:
        table[s_result["Game ID"]] = table_values

table_data = get_table_data(t_player_class)
graph_data = get_graph_data(t_player_class)
key_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
table = get_table(table_data, key_list)
graph = get_graph(graph_data, key_list)
graph_count = get_graph_count(key_list)

a = 0
