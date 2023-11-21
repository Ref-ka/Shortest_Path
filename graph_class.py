from pandas import DataFrame, set_option
from collections import deque

set_option('display.max_rows', None, 'display.max_columns', None)


def make_matrix(dist, history) -> tuple:
    if history:
        history = DataFrame(list(x for x in history)).set_axis(list(f'Шаг {x}' for x in range(1, len(history) + 1)))
    return DataFrame(list(x for x in dist)), history


class Graph:

    # Иницилизируем объект класса Graph

    def __init__(self, vertices):
        self.V = vertices
        self.graph = {}

    # Метод добавления ребра в граф

    def add_edge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append([v, w])
        self.graph[u] = sorted(self.graph[u])

    # Метод отображения ответа

    def print_spfa(self, dist):
        ans = 'Расстояние\n от выбранной вершины\n до остальных\n'
        for i in range(self.V):
            ans += "% d \t\t % d" % (i, dist[i]) + '\n'
        return ans

    # Метод получения ответа, алгоритм поиска кратчайших путей

    def spfa(self, src):
        dist = [float('inf')] * self.V
        dist[src] = 0
        q = deque()
        q.append(src)
        counter = 0
        dist_history = list()
        dist_history.append(dist[:])
        length = {}
        while q:
            counter += 1
            u = q.popleft()
            if u in self.graph:
                for v, w in self.graph[u]:
                    if dist[u] != float('inf') and dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        if v not in q:
                            q.append(v)
                            if v not in length:
                                length[v] = 1
                            else:
                                length[v] += 1
                            if length[v] == self.V:
                                return DataFrame(), ''
                            counter += 1
            dist_history.append(dist[:])
        return make_matrix(dist, dist_history)

    def wfi(self):
        dist = []

        for i in range(self.V):
            dist.append([float('inf')] * self.V)
            dist[i][i] = 0

        for i in self.graph:
            for j, k in self.graph[i]:
                dist[i][j] = k

        for i in range(self.V):
            for j in range(self.V):
                for k in range(self.V):
                    if dist[k][k] < 0:
                        return DataFrame(), ''
                    dist[j][k] = min(dist[j][k], dist[j][i] + dist[i][k])

        return make_matrix(dist, '')
