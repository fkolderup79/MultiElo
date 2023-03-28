from datetime import datetime


def get_table_data(t_player_class):
    count = 0
    table_data = []
    game_id = ''
    t_player_sorted = get_player_sorted(t_player_class)
    for s_player_sorted in t_player_sorted:
        Player = s_player_sorted["Player"]
        count += 1
        game_id = ''
        win = ''
        win_count = 0
        point = ''
        point_count = 0
        elo_total = 0
        elo_high = 0
        elo_low = 9999
        elo_count = 0
        elo_perf_count = 0
        pos_win = 0
        pos_total = 0
        for s_elo in Player.t_elo:
            if s_elo["Game ID"] != game_id:
                if win == 'X':
                    win_count += 1
                if s_elo["Points"] < 0:
                    win = ''
                else:
                    win = 'X'
                game_id = s_elo["Game ID"]
            else:
                if s_elo["Points"] < 0:
                    win = ''
        if win == 'X':
            win_count += 1
        for s_elo in Player.t_elo:
            if s_elo["Game ID"] != game_id:
                if point == 'X':
                    point_count += 1
                if s_elo["Points"] > 0:
                    point = 'X'
                else:
                    point = ''
                game_id = s_elo["Game ID"]
            else:
                if s_elo["Points"] > 0:
                    point = 'X'
        if point == 'X':
            point_count += 1
        for s_elo_game in Player.t_elo_game:
            if s_elo_game["ELO"] > elo_high:
                elo_high = s_elo_game["ELO"]
            if s_elo_game["ELO"] < elo_low:
                elo_low = s_elo_game["ELO"]
            if s_elo_game["Count"] > 1 and s_elo_game["Position"] > 0:
                pos_win = pos_win + s_elo_game["Count"] - s_elo_game["Position"]
                pos_total = pos_total + s_elo_game["Count"] - 1
        pos_perct = round((pos_win / pos_total)*100)
        pos_perct = str(pos_perct) + '%'
        win_perct = round((win_count / Player.game_count)*100)
        win_perct = str(win_perct) + '%'
        point_perct = round((point_count / Player.game_count)*100)
        point_perct = str(point_perct) + '%'
        if count == 1:
            table_data = {count: [Player.id, Player.game_count, Player.elo, Player.elo_average, elo_high, elo_low, win_count, win_perct, point_count, point_perct, pos_perct]}
        else:
            table_data[count] = [Player.id, Player.game_count, Player.elo, Player.elo_average, elo_high, elo_low, win_count, win_perct, point_count, point_perct, pos_perct]
    return table_data


def get_graph_data(t_player_class):
    graph_data = []
    t_player_sorted = get_player_sorted(t_player_class)
    data = []
    count = 0
    s_player_sorted = t_player_sorted[count]
    for s_elo_game in s_player_sorted["Player"].t_elo_game:
        data.append(s_elo_game["Game ID"])
    graph_data = {count: data}
    for s_player_sorted in t_player_sorted:
        data = []
        for s_elo_game in s_player_sorted["Player"].t_elo_game:
            data.append(s_elo_game["ELO"])
        count += 1
        graph_data[count] = data
    return graph_data


def convert_table_data(string):
    skip_count = 1
    find_key = 'X'
    find_values = ''
    key = ''
    values = ''
    key_part = ''
    value_part = ''
    key_completed = ''
    values_completed = ''
    table_count = 0
    values = []
    for l in string:
        if skip_count > 0:
            skip_count -= 1
        else:
            if find_key == 'X':
                if l == ":":
                    key = key_part
                    key_completed = 'X'
                    find_key = ''
                    find_values = 'X'
                    skip_count = 2
                else:
                    key_part = key_part + l
            elif find_values == 'X':
                if l == ",":
                    values.append(value_part)
                    value_part = ''
                elif l == ']':
                    values.append(value_part)
                    values_completed = 'X'
                elif l != "'":
                    value_part = value_part + l
            if key_completed == 'X':
                if values_completed == 'X':
                    if table_count == 0:
                        table_count += 1
                        table_data = {int(key): values}
                    else:
                        table_data[int(key)] = values
                    key = ''
                    values = []
                    key_part = ''
                    value_part = ''
                    find_key = 'X'
                    find_values = ''
                    key_completed = ''
                    values_completed = ''
                    skip_count = 2
    return table_data


def convert_graph_data(string):
    skip_count = 1
    find_key = 'X'
    find_values = ''
    key = ''
    values = ''
    key_part = ''
    value_part = ''
    key_completed = ''
    values_completed = ''
    table_count = 0
    values = []
    for l in string:
        if skip_count > 0:
            skip_count -= 1
        else:
            if find_key == 'X':
                if l == ":":
                    key = key_part
                    key_completed = 'X'
                    find_key = ''
                    find_values = 'X'
                    skip_count = 2
                else:
                    key_part = key_part + l
            elif find_values == 'X':
                if l == ",":
                    values.append(int(value_part))
                    value_part = ''
                elif l == ']':
                    values.append(int(value_part))
                    values_completed = 'X'
                elif l != "'":
                    value_part = value_part + l
            if key_completed == 'X':
                if values_completed == 'X':
                    if table_count == 0:
                        table_count += 1
                        table_data = {int(key): values}
                    else:
                        table_data[int(key)] = values
                    key = ''
                    values = []
                    key_part = ''
                    value_part = ''
                    find_key = 'X'
                    find_values = ''
                    key_completed = ''
                    values_completed = ''
                    skip_count = 2
    return table_data


def get_table(table_data, key_list):
    table = []
    count = 0
    player_count = 0
#    table_data = get_table_data(table_data_string)
    for key, values in table_data.items():
        count += 1
        found = ''
        table_values = []
        for v in values:
            table_values.append(v)
            break
        if player_count < 10:
            for k in key_list:
                if k == str(key):
                    found = 'X'
                    break
        if found == 'X':
            player_count += 1
            graph_sel = "&FlagSet&"
            table_values.append(graph_sel)
            graph_id = 'Player ' + str(player_count)
            table_values.append(graph_id)
        else:
            graph_sel = "&FlagNot&"
            table_values.append(graph_sel)
            graph_id = ''
            table_values.append(graph_id)
        value_count = 0
        for v in values:
            value_count += 1
            if value_count > 1:
                table_values.append(v)
        if count == 1:
            table = {key: table_values}
        else:
            table[key] = table_values
    return table


def get_graph(graph_data, key_list):
    graph = []
    graph_count = 0
    for key, values in graph_data.items():
        if int(key) == 0:
            graph.append({"labels": values})
            label_values = values
            continue
        key_found = ''
        for k in key_list:
            if k == str(key):
                key_found = 'X'
                break
        if key_found == 'X':
            graph_count += 1
            graph_key = 'data' + str(graph_count)
            graph.append({graph_key: values})
    while graph_count < 10:
        graph_count += 1
        graph_values = []
        for v in label_values:
            graph_values.append(1000)
        graph_key = 'data' + str(graph_count)
        graph.append({graph_key: graph_values})
    return graph


def get_table_game(t_result):
    table = []
    count_high = 0
    for key, values in t_result.items():
        count = 0
        for v in values:
            count += 1
            if count > count_high:
                count_high = count
    for key, values in t_result.items():
        count = 0
        table_values = []
        for v in values:
            count += 1
            table_values.append(v)
        count_remain = count_high - count
        while count_remain > 0:
            count_remain -= 1
            table_values.append("")
        if key == 1:
            table = {key: table_values}
        else:
            table[key] = table_values
    return table


def get_graph_count(key_list):
    graph_count = 0
    for k in key_list:
        graph_count += 1
    return graph_count


def get_player_sorted(t_player_class):
    t_player_sorted_count = []
    t_player_sorted = []
    for s_player_class in t_player_class:
        t_player_sorted_count.append({'Player': s_player_class['Player'], 'count': s_player_class['Player'].game_count})
    t_player_sorted_count.sort(reverse=True, key=lambda x: x.get('count'))
    for s_player_sorted_count in t_player_sorted_count:
        t_player_sorted.append({"Player": s_player_sorted_count["Player"]})
    return t_player_sorted


def get_pos_count(t_result):
    pos_count = 0
    for key, values in t_result.items():
        game_pos_count = -3
        for v in values:
            game_pos_count += 1
        if game_pos_count > pos_count:
            pos_count = game_pos_count
    return pos_count


def convert_table_game_date(table_game):
    table = []
    for key, values in table_game.items():
        table_values = []
        v_count = 0
        for v in values:
            v_count += 1
            if v_count == 1:
                c_count = 0
                date_str = ''
                for c in v:
                    c_count += 1
                    if 15 <= c_count <= 18:
                        date_str = date_str + c
                date_str = date_str + '-'
            elif v_count == 2:
                for c in v:
                    if c != ' ':
                        date_str = date_str + c
                    else:
                        date_str = date_str + '0'
                date_str = date_str + '-'
            elif v_count == 3:
                for c in v:
                    if c == ')':
                        continue
                    elif c != ' ':
                        date_str = date_str + c
                    else:
                        date_str = date_str + '0'
                    try:
                        datetime = datetime.strptime(date_str, "%Y-%m-%d")
                        v = datetime.date()
                    except UnboundLocalError:
                        v = date_str
                table_values.append(v)
            else:
                table_values.append(v)
        if table == []:
            table = {key: table_values}
        else:
            table[key] = table_values
    return table


def get_table_player_data(t_player):
    count = 0
    t_header_values = []
    t_header_values.append("Total Points")
    for s_player_win in t_player:
        count += 1
        t_header_values.append(s_player_win["Player"].id)
        t_values = []
        t_values.append(s_player_win["Player"].elo-s_player_win["Player"].class_elo.base)
        for s_player_loose in t_player:
            if s_player_loose["Player"] == s_player_win["Player"]:
                t_values.append('N/A')
            else:
                points = 0
                for s_elo in s_player_win["Player"].t_elo:
                    if s_elo["Player"] == s_player_loose["Player"]:
                        points += s_elo["Points"]
                points = round(points * s_player_win["Player"].class_elo.m)
                t_values.append(points)
            if count == 1:
                t_table_player_data = {count: t_values}
            else:
                t_table_player_data[count] = t_values
        t_table_player_data[0] = t_header_values
    return t_table_player_data


def get_table_player(table_player_data, key_list):
    table = []
    count = 0
    player_count = 0
#    table_data = get_table_data(table_data_string)
    for key, values in sorted(table_player_data.items()):
        table_values = []
        if key == 0:
            table_values.append('')
            header_values = values
            for k in key_list:
                count = -1
                for v in values:
                    count += 1
                    if k == str(count):
                        table_values.append(v)
                        continue
            table_values.append('Others')
            table = {0: table_values}
            count = 0
            continue
        count += 1
        found = ''
        if player_count < 10:
            for k in key_list:
                if k == str(key):
                    found = 'X'
                    my_key = k

                    break
        if found == 'X':
            table_values = []
#            for k in key_list:
#                if k == my_key:
#                    table_values.append('N/A')
            table_values.append(header_values[int(my_key)])
            v_count = -1
            for v in values:
                v_count += 1
                if v_count == 0:
                    v_others = v
                    continue
                if str(v_count) == my_key:
                    table_values.append('N/A')
                    continue
                found = ''
                for k2 in key_list:
                    if k2 == str(v_count):
                        found = 'X'
                        break
                if found == 'X':
                    table_values.append(v)
                    v_others -= v
            table_values.append(v_others)
            if table == []:
                table = {count: table_values}
            else:
                table[count] = table_values
    return table


def get_table_player_data2(t_player):
    count = 0
    t_header_values = []
    for s_player_win in t_player:
        count += 1
        t_header_values.append(s_player_win["Player"].id)
        t_values = []
        for s_player_loose in t_player:
            if s_player_loose["Player"] == s_player_win["Player"]:
                t_values.append('N/A')
            else:
                points = 0
                for s_elo in s_player_win["Player"].t_elo:
                    if s_elo["Player"] == s_player_loose["Player"]:
                        points += s_elo["Points"]
                points = round(points * s_player_win["Player"].class_elo.m)
                t_values.append(points)
            if count == 1:
                t_table_player_data = {count: t_values}
            else:
                t_table_player_data[count] = t_values
        t_table_player_data[0] = t_header_values
    return t_table_player_data