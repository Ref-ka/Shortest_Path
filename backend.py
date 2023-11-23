from graph_class import Graph
from front import View
from info_class import Info
from tkinter import filedialog
import time


class Back:
    def __init__(self, view, info):
        self.view = view
        self.info = info

    def start(self):
        self.view.setup(self)
        self.view.start_main_loop()

# Info methods
    def connection_check(self, var) -> bool:
        return self.info.connection_check(var)

    def insert_connection(self, var):
        self.info.insert_connection(var)

    def clear(self):
        self.info.clear()
        self.view.clear()

    def delete_connection(self, var):
        self.info.delete_connection(var)

    def get_vertexes(self) -> list:
        return self.info.get_vertexes()

    def get_vertexes_count(self) -> int:
        return self.info.get_vertexes_count()

    def insert_src(self, src):
        self.info.insert_src(src)

    def get_connections(self) -> list:
        return self.info.get_connections()

    def get_src(self) -> int:
        return self.info.get_src()

# View methods
    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.clear()
            with open(file_path, 'r') as file:
                start = time.monotonic()
                for line in file.readlines():
                    self.input_connection_command(line.replace('\n', ''))
                print(f'load_connection_time: {time.monotonic() - start}')
    def input_connection_command(self, file_var=None):
        self.view.input_connection_command(self, file_var)

    def input_src_command(self):
        self.view.input_src_command(self)

    def get_answer(self, wfi=None):
        self.view.get_answer(self, wfi)

    def get_answer_wfi(self):
        self.get_answer(True)

# Graph methods
    def make_graph(self, wfi) -> tuple:
        #  Создаем объект класса Graph и получаем ответ
        g = Graph(self.get_vertexes_count())
        for line in self.get_connections():
            g.add_edge(line[0], line[1], line[2])
        if not wfi:
            return g.spfa(int(self.get_src()))
        else:
            return g.wfi()


back = Back(View(), Info())
back.start()
