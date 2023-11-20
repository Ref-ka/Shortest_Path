import time

import networkx as nx
from algorithm import Graph
import matplotlib.pyplot as plt
from io import BytesIO


def make_graph_image(g):          # SO SLOW!!!
    #  Создаем визуализацию нашего графа

    g_vis = nx.DiGraph(directed=True)

    # Добавляем вершины и ребра в визуализацию

    edge_labels = {}
    for ver in g.graph:
        g_vis.add_node(ver)
    for ver1 in g.graph:
        for line in g.graph[ver1]:
            g_vis.add_edge(ver1, line[0])
            edge_labels[(ver1, line[0])] = line[1]

    # Задаём позиционирование графа

    pos = nx.shell_layout(g_vis)

    # Отрисовываем граф и значения ребер, сохраняем изображение графа

    nx.draw(g_vis, pos, with_labels=True, node_color='#29BCFF', node_size=1250)

    nx.draw_networkx_edge_labels(g_vis, pos, edge_labels=edge_labels,
                                 font_size=9, font_color='#151E3D', label_pos=0.3,
                                 bbox=dict(facecolor='white', edgecolor='none', pad=0.5))

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    return buf


def make_graph(vert, input_info, src, wfi) -> tuple:
    #  Создаем объект класса Graph и получаем ответ

    g = Graph(int(vert))
    for line in input_info:
        g.add_edge(line[0], line[1], line[2])
    if not wfi:
        ans, history = g.spfa(int(src))
    else:

        ans, history = g.wfi()

    buf = make_graph_image(g)

    return ans, history, buf
