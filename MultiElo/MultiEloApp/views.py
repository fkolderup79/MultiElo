from django.shortcuts import render
from django.http import HttpResponse

from .data_excel import calc_excel
from .data_static import calc_static
from .html_main import get_table
from .html_main import get_graph
from .html_main import get_table_data
from .html_main import get_graph_data
from .html_main import convert_table_data
from .html_main import convert_graph_data
from .html_main import get_graph_count
from .html_main import get_table_game
from .html_main import get_pos_count
from .html_main import convert_table_game_date
#from .html_main import get_table_player_data
#from .html_main import get_table_player


#def test(request):
#    return HttpResponse("Test 123")
def faq(request):
    return render(request, 'faq.html')


def game(request):
    if request.method == 'GET':
        t_player_class, t_result = calc_static()
        table_data = get_table_data(t_player_class)
        graph_data = get_graph_data(t_player_class)
        #        table_player_data = get_table_player_data(t_player_class)
        key_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        table_game = get_table_game(t_result)
    else:
        if "Upload" in request.POST:
            uploaded_file = request.FILES["document"]
            t_player_class, t_result = calc_excel(uploaded_file)
            table_data = get_table_data(t_player_class)
            graph_data = get_graph_data(t_player_class)
            #            table_player_data = get_table_player_data(t_player_class)
            key_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            table_game = get_table_game(t_result)
        else:
            key_list = request.POST.getlist('boxes')
            table_data_string = request.POST.get('table_data')
            table_data = convert_table_data(table_data_string)
            graph_data_string = request.POST.get('graph_data')
            graph_data = convert_graph_data(graph_data_string)
            table_game_string = request.POST.get('table_game')
            table_game = convert_table_data(table_game_string)
            #            table_game = convert_table_game_date(table_game)
            t_result_string = request.POST.get('t_result')
            t_result = convert_table_data(t_result_string)
    table = get_table(table_data, key_list)
    graph = get_graph(graph_data, key_list)
    graph_count = get_graph_count(key_list)
    pos_count = get_pos_count(t_result)
    #    table_player = get_table_player(table_player_data, key_list)
    for a in graph:
        for b in a:
            e = b
        if e == "labels":
            labels = a["labels"]
        elif e == "data1":
            data1 = a["data1"]
        elif e == "data2":
            data2 = a["data2"]
        elif e == "data3":
            data3 = a["data3"]
        elif e == "data4":
            data4 = a["data4"]
        elif e == "data5":
            data5 = a["data5"]
        elif e == "data6":
            data6 = a["data6"]
        elif e == "data7":
            data7 = a["data7"]
        elif e == "data8":
            data8 = a["data8"]
        elif e == "data9":
            data9 = a["data9"]
        elif e == "data10":
            data10 = a["data10"]
        label1 = '"TestLabel"'
    return render(request, 'game.html', {
        'labels': labels,
        'label1': label1,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6,
        'data7': data7,
        'data8': data8,
        'data9': data9,
        'data10': data10,
        'table': table,
        'table_game': table_game,
        'table_data': table_data,
        'graph_data': graph_data,
        'graph_count': graph_count,
        't_result': t_result,
        'pos_count': pos_count,
    })


def about(request):
    return render(request, 'about.html')


def main(request):
    if request.method == 'GET':
        t_player_class, t_result = calc_static()
        table_data = get_table_data(t_player_class)
        graph_data = get_graph_data(t_player_class)
#        table_player_data = get_table_player_data(t_player_class)
        key_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        table_game = get_table_game(t_result)
    else:
        if "Upload" in request.POST:
            uploaded_file = request.FILES["document"]
            t_player_class, t_result = calc_excel(uploaded_file)
            table_data = get_table_data(t_player_class)
            graph_data = get_graph_data(t_player_class)
#            table_player_data = get_table_player_data(t_player_class)
            key_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            table_game = get_table_game(t_result)
        else:
            key_list = request.POST.getlist('boxes')
            table_data_string = request.POST.get('table_data')
            table_data = convert_table_data(table_data_string)
            graph_data_string = request.POST.get('graph_data')
            graph_data = convert_graph_data(graph_data_string)
            table_game_string = request.POST.get('table_game')
            table_game = convert_table_data(table_game_string)
#            table_game = convert_table_game_date(table_game)
            t_result_string = request.POST.get('t_result')
            t_result = convert_table_data(t_result_string)
    table = get_table(table_data, key_list)
    graph = get_graph(graph_data, key_list)
    graph_count = get_graph_count(key_list)
    pos_count = get_pos_count(t_result)
#    table_player = get_table_player(table_player_data, key_list)
    for a in graph:
        for b in a:
            e = b
        if e == "labels":
            labels = a["labels"]
        elif e == "data1":
            data1 = a["data1"]
        elif e == "data2":
            data2 = a["data2"]
        elif e == "data3":
            data3 = a["data3"]
        elif e == "data4":
            data4 = a["data4"]
        elif e == "data5":
            data5 = a["data5"]
        elif e == "data6":
            data6 = a["data6"]
        elif e == "data7":
            data7 = a["data7"]
        elif e == "data8":
            data8 = a["data8"]
        elif e == "data9":
            data9 = a["data9"]
        elif e == "data10":
            data10 = a["data10"]
        label1 = '"TestLabel"'
    return render(request, 'main.html', {
        'labels': labels,
        'label1': label1,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6,
        'data7': data7,
        'data8': data8,
        'data9': data9,
        'data10': data10,
        'table': table,
        'table_game': table_game,
        'table_data': table_data,
        'graph_data': graph_data,
        'graph_count': graph_count,
        't_result': t_result,
        'pos_count': pos_count,
    })