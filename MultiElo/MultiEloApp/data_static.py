from datetime import datetime
from .multielo import calculate


def calc_static():
    s_settings = {'K-factor': 10, 'E-factor': 400, 'ELO Base': 1000, 'Multiplier': 1}

    t_distr = []
    t_distr.append({'Count From': 2, 'Position To': 1, 'Distribution': 100})
    t_distr.append({'Count From': 3, 'Position To': 1, 'Distribution': 70})
    t_distr.append({'Count From': 3, 'Position To': 2, 'Distribution': 30})
    t_distr.append({'Count From': 8, 'Position To': 1, 'Distribution': 55})
    t_distr.append({'Count From': 8, 'Position To': 2, 'Distribution': 30})
    t_distr.append({'Count From': 8, 'Position To': 3, 'Distribution': 15})

    import random

    index = 0
    t_player_pos = []
    t_player_in = []
    t_result = []

    def add_player_init(t_player, index_start, index_num, id):
        index = index_start
        count = 0
        values = []
        values.append(id)
        while count < index_num:
            index += 1
            count += 1
            if t_player == []:
                t_player = {index: values}
            else:
                t_player[index] = values
        return t_player, index

    def add_player_rest(t_player, index, index_max):
        while index < index_max:
            values = []
            index += 1
            random_num = random.randint(1, 10)
            if random_num == 1:
                values.append('Mary')
            elif random_num == 2:
                values.append('James')
            elif random_num == 3:
                values.append('Patricia')
            elif random_num == 4:
                values.append('Jennifer')
            elif random_num == 5:
                values.append('Robert')
            elif random_num == 6:
                values.append('Linda')
            elif random_num == 7:
                values.append('John')
            elif random_num == 8:
                values.append('Michael')
            elif random_num == 9:
                values.append('Elizabeth')
            elif random_num == 10:
                values.append('David')
            if t_player == []:
                t_player = {index: values}
            else:
                t_player[index] = values
        return t_player

    t_player_pos, index = add_player_init(t_player_pos, index, 15, 'Mary')
    t_player_pos, index = add_player_init(t_player_pos, index, 13, 'James')
    t_player_pos, index = add_player_init(t_player_pos, index, 10, 'Patricia')
    t_player_pos, index = add_player_init(t_player_pos, index, 9, 'Jennifer')
    t_player_pos, index = add_player_init(t_player_pos, index, 8, 'Robert')
    t_player_pos, index = add_player_init(t_player_pos, index, 7, 'Linda')
    t_player_pos, index = add_player_init(t_player_pos, index, 6, 'John')
    t_player_pos, index = add_player_init(t_player_pos, index, 5, 'Michael')
    t_player_pos, index = add_player_init(t_player_pos, index, 2, 'Elizabeth')
    t_player_pos, index = add_player_init(t_player_pos, index, 1, 'David')

    t_player_pos = add_player_rest(t_player_pos, index, 100)

    index = 0
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Mary')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'James')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Patricia')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Jennifer')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Robert')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Linda')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'John')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Michael')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'Elisabeth')
    t_player_in, index = add_player_init(t_player_in, index, 1, 'David')

    t_player_in = add_player_rest(t_player_in, index, 30)

    game_num = 0

    while game_num < 100:
        game_num += 1
        count = 0
        t_player = []
        t_player_order = []
        player_count = random.randint(5, 10)
        while count < player_count:
            random_index = random.randint(1, 30)
            for key, values in t_player_in.items():
                if key == random_index:
                    break
            for v in values:
                id = v
            found = ''
            for s_player in t_player:
                if s_player[0] == id:
                    found = 'X'
                    break
            if found == '':
                t_player.append([id])
                count += 1
        count = 0
        while count < player_count:
            random_index = random.randint(1, 100)
            for key, values in t_player_pos.items():
                if key == random_index:
                    break
            for v in values:
                id = v
            for s_player in t_player:
                if s_player[0] == id:
                    found = 'X'
                    break
            if found == 'X':
                found = ''
                for s_player_order in t_player_order:
                    if s_player_order[0] == id:
                        found = 'X'
                        break
                if found == '':
                    t_player_order.append([id])
                    count += 1
        data = []
        data.append('')
        data.append(player_count)
        if player_count > 8:
            data.append('55-30-15')
        else:
            data.append('70-30')
        for s_player_order in t_player_order:
            data.append(s_player_order[0])
        if t_result == []:
            t_result = {game_num: data}
        else:
            t_result[game_num] = data

    t_player = calculate(s_settings, t_result, t_distr)

    return t_player, t_result