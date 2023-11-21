import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from pandas import DataFrame, set_option
from collections import deque

set_option('display.max_rows', None, 'display.max_columns', None)


def make_matrix(dist, history) -> tuple:
    if history:
        history = DataFrame(list(x for x in history)).set_axis(list(f'Шаг {x}' for x in range(1, len(history) + 1)))
    return DataFrame(list(x for x in dist)), history


def make_image(g) -> BytesIO:          # SO SLOW!!!
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


class Graph:

    # Иницилизируем объект класса Graph

    def __init__(self, vertices):
        self.V = vertices
        self.graph = {}
        self.dist = []
        self.history = []

    # Метод добавления ребра в граф

    def add_edge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append([v, w])
        self.graph[u] = sorted(self.graph[u])

    # Метод отображения ответа

    def make_answer(self) -> tuple:
        matrices = make_matrix(self.dist, self.history)
        return matrices[0], matrices[1], make_image(self)

    # Метод получения ответа, алгоритм поиска кратчайших путей

    def spfa(self, src) -> tuple:
        self.dist = [float('inf')] * self.V
        self.dist[src] = 0
        q = deque()
        q.append(src)
        counter = 0
        self.history.append(self.dist[:])
        length = {}
        while q:
            counter += 1
            u = q.popleft()
            if u in self.graph:
                for v, w in self.graph[u]:
                    if self.dist[u] != float('inf') and self.dist[u] + w < self.dist[v]:
                        self.dist[v] = self.dist[u] + w
                        if v not in q:
                            q.append(v)
                            if v not in length:
                                length[v] = 1
                            else:
                                length[v] += 1
                            if length[v] == self.V:
                                return DataFrame(), ''
                            counter += 1
            self.history.append(self.dist[:])
        return self.make_answer()

    def wfi(self) -> tuple:
        for i in range(self.V):
            self.dist.append([float('inf')] * self.V)
            self.dist[i][i] = 0

        for i in self.graph:
            for j, k in self.graph[i]:
                self.dist[i][j] = k

        for i in range(self.V):
            for j in range(self.V):
                for k in range(self.V):
                    if self.dist[k][k] < 0:
                        return DataFrame(), ''
                    self.dist[j][k] = min(self.dist[j][k], self.dist[j][i] + self.dist[i][k])

        return self.make_answer()
