from graph_class import Graph
from front import View, make_new_window
from info_class import Info
from tkinter import filedialog
import time
import cProfile


class Back:
    def __init__(self, view, info):
        self.view = view
        self.info = info

    def start(self):
        self.view.setup(self)
        self.view.start_main_loop()

# Info methods
    def info_connection_check(self, var) -> bool:
        return self.info.connection_check(var)

    def info_insert_connection(self, var):
        self.info.insert_connection(var)

    def info_delete_connection(self, var):
        self.info.delete_connection(var)

    def info_get_vertexes(self) -> list:
        return self.info.get_vertexes()

    def info_get_vertexes_count(self) -> int:
        return self.info.get_vertexes_count()

    def info_insert_src(self, src):
        self.info.insert_src(src)

    def info_get_connections(self) -> list:
        return self.info.get_connections()

    def info_get_src(self) -> int:
        return self.info.get_src()

# View methods
    def get_answer(self, wfi=False):
        if self.info.get_connections() and (self.info.get_src() != None or wfi):
            ans, history, buf = back.make_graph(wfi)
            self.view.show_answer(ans, history, buf, wfi)
        else:
            make_new_window('Вы не ввели некоторые данные!\n''Проверьте все колонки ввода!')

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.clear()
            with open(file_path, 'r') as file:
                start = time.monotonic()
                data = file.readlines()
                for i, line in enumerate(data):
                    if i == len(data) - 1:
                        self.input_connection_command(self, line.replace('\n', ''), True)
                    else:
                        self.input_connection_command(self, line.replace('\n', ''))
                print(f'load_connection_time: {time.monotonic() - start}')

    def input_connection_command(self, var, file_var=None, last=None):
        try:
            if not file_var:
                var = list(map(int, var))
            else:
                var = list(map(int, file_var.split()))
        except ValueError:
            make_new_window('Введенные или загруженные\nданные неверны!')
            var = None
        if var and len(var) == 3 and var[0] != var[1]:
            if not self.info.connection_check(var):
                self.info.insert_connection(var)
                if last:
                    new_info = ''
                    for line in self.info.get_connections():
                        new_info += ' '.join(str(x) for x in line) + '\n'
                    self.view.change_input_info_scrl_label(new_info)
                if not file_var:
                    self.view.change_input_info_scrl_label(' '.join(str(x) for x in var) + '\n', True)
            else:
                self.info.delete_connection(var)
                new_info = ''
                for line in self.info.get_connections():
                    new_info += ' '.join(str(x) for x in line) + '\n'
                self.view.change_input_info_scrl_label(new_info)
        else:
            make_new_window('В полученных данных есть ошибки!\nНекорректные данные были удалены из списка\n'
                            'Вы можете очистить эти данные или продолжить работать с ними')
        self.view.change_vertex_count_label(self.info.get_vertexes_count())

    def input_src_command(self, src):
        try:
            src = int(src)
            if src in self.info.get_vertexes():
                self.info.insert_src(src)
                self.view.change_src_entry(src)
            else:
                make_new_window('Данной вершины нет в графе!')
        except ValueError:
            make_new_window('Данные введены неверно!')

# Graph methods
    def make_graph(self, wfi) -> tuple:
        draw = self.view.draw_switch.get()
        #  Создаем объект класса Graph и получаем ответ
        g = Graph(self.info_get_vertexes_count())
        for line in self.info_get_connections():
            g.add_edge(line[0], line[1], line[2])
        if not wfi:
            return g.spfa(int(self.info_get_src()), draw)
        else:
            return g.wfi(draw)

# Global methods
    def clear(self):
        self.info.clear()
        self.view.clear()


if __name__ == '__main__':
    back = Back(View(), Info())
    cProfile.run('back.start()', sort='cumtime')
