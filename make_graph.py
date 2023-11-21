import networkx as nx
from algorithm import Graph
import matplotlib.pyplot as plt
from io import BytesIO
from front import View, load_file
from info_class import Info


class Back:
    def __init__(self, view, info):
        self.view = view
        self.info = info

    def start(self):
        self.view.setup(self)
        self.view.start_main_loop()

# Methods with info
    def connection_check(self, var):
        return self.info.connection_check(var)

    def insert_connection(self, var):
        self.info.insert_connection(var)

    def clear(self):
        self.info.clear()
        self.view.clear()

    def delete_connection(self, var):
        self.info.delete_connection(var)

    def get_vertexes(self):
        return self.info.get_vertexes()

    def get_vertexes_count(self):
        return self.info.get_vertexes_count()

    def insert_src(self, src):
        self.info.insert_src(src)

    def get_connections(self):
        return self.info.get_connections()

    def get_src(self):
        return self.info.get_src()

# Methods with view
    def load_file(self):
        load_file(self)

    def input_connection_command(self, file_var=None):
        self.view.input_connection_command(self, file_var)

    def input_src_command(self):
        self.view.input_src_command(self)

    def get_answer(self, wfi=None):
        self.view.get_answer(self, wfi)

    def get_answer_wfi(self):
        self.get_answer(True)

# Methods with graph
    def make_graph_image(self, g):          # SO SLOW!!!
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

    def make_graph(self, vert, input_info, src, wfi) -> tuple:
        #  Создаем объект класса Graph и получаем ответ
        g = Graph(int(vert))
        for line in input_info:
            g.add_edge(line[0], line[1], line[2])
        if not wfi:
            ans, history = g.spfa(int(src))
        else:
            ans, history = g.wfi()

        buf = self.make_graph_image(g)

        return ans, history, buf


back = Back(View(), Info())
back.start()
