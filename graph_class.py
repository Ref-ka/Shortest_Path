import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from pandas import DataFrame, set_option
from collections import deque

set_option('display.max_rows', None, 'display.max_columns', None)


def make_matrix(dist, history, src) -> tuple:  # Make DataFrame from list for visualisation
    if history:
        history = DataFrame(list(x for x in history)).set_axis(list(f'Шаг {x}' for x in range(1, len(history) + 1)))
    if src:
        return DataFrame(list(x for x in dist)).set_axis(list(str(src)), axis='columns'), history
    return DataFrame(list(x for x in dist)), history


def make_image(g) -> BytesIO:  # Make and save an image from graph for its visualisation
    g_vis = nx.DiGraph(directed=True)  # Make visualisation

    edge_labels = {}  # Add vertexes and edges to visualisation
    for ver in g.connections:
        g_vis.add_node(ver)
    for ver1 in g.connections:
        for line in g.connections[ver1]:
            g_vis.add_edge(ver1, line[0])
            edge_labels[(ver1, line[0])] = line[1]

    pos = nx.shell_layout(g_vis)  # Make a position layout for visualisation

    nx.draw(g_vis, pos, with_labels=True, node_color='#29BCFF', node_size=700)  # Draw a graph
    nx.draw_networkx_edge_labels(g_vis, pos, edge_labels=edge_labels,
                                 font_size=9, font_color='#151E3D', label_pos=0.3,
                                 bbox=dict(facecolor='white', edgecolor='none', pad=0.5))

    buf = BytesIO()  # Save a visualisation
    plt.savefig(buf, format='png')
    plt.clf()
    return buf


class Graph:

    def __init__(self, vertexes):
        self.v_amount = vertexes
        self.connections = {}
        self.dist = []
        self.history = []

    def add_edge(self, u, v, w):
        if u not in self.connections:
            self.connections[u] = []
        self.connections[u].append([v, w])
        self.connections[u] = sorted(self.connections[u])

    def _make_answer(self, draw, negative_cycle=None, src=None) -> tuple:  # Connect the data and make answer
        if negative_cycle:  # Return empty data if negative cycle was found
            return DataFrame(), '', None
        matrices = make_matrix(self.dist, self.history, src)
        if draw:  # Check if we don't need a visualisation of graph
            return matrices[0], matrices[1], None
        else:
            return matrices[0], matrices[1], make_image(self)

    def spfa(self, src, draw) -> tuple:
        self.dist = [float('inf')] * self.v_amount  # Make a default list of distances between vertexes
        self.dist[src] = 0

        q = deque()  # Make a queue for updated vertexes
        q.append(src)

        self.history.append(self.dist[:])  # List for save history of algorythm steps

        length = {}  # Dict for check if there is negative cycle in graph
        while q:
            u = q.popleft()
            if u in self.connections:
                for v, w in self.connections[u]:
                    if self.dist[u] != float('inf') and self.dist[u] + w < self.dist[v]:
                        self.dist[v] = self.dist[u] + w
                        if v not in q:
                            q.append(v)
                            if v not in length:
                                length[v] = 1
                            else:
                                length[v] += 1
                            if length[v] == self.v_amount:
                                return self._make_answer(draw, True)
            self.history.append(self.dist[:])
        return self._make_answer(draw, src=src)

    def wfi(self, draw) -> tuple:
        for i in range(self.v_amount):  # Make a default matrix
            self.dist.append([float('inf')] * self.v_amount)
            self.dist[i][i] = 0
        for i in self.connections:  # Add available connections to default matrix
            for j, k in self.connections[i]:
                self.dist[i][j] = k
        for i in range(self.v_amount):
            for j in range(self.v_amount):
                for k in range(self.v_amount):
                    if self.dist[k][k] < 0:
                        return self._make_answer(draw, True)
                    self.dist[j][k] = min(self.dist[j][k], self.dist[j][i] + self.dist[i][k])
        return self._make_answer(draw)
