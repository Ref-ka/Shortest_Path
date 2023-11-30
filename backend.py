from graph_class import Graph
from front import View, make_new_window
from info_class import Info
from tkinter import filedialog
import cProfile


class Back:
    def __init__(self, view, info):
        self.view = view
        self.info = info

    def start(self):
        self.view.setup(self)
        self.view.start_main_loop()

    def get_answer(self, wfi=False):
        if self.info.get_connections() and ((self.info.get_src() is not None) or wfi):  # If all needed info exist
            ans, history, buf = self._make_graph(wfi)  # Get data and image for visualisation
            self.view.show_answer(ans, history, buf, wfi)  # Visualisation of answer
        else:  # Exception if some of needed info doesn't exist
            make_new_window('Вы не ввели некоторые данные!\n''Проверьте все колонки ввода!')

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:  # If file path was chosen
            self.clear()  # Clear all old information
            with open(file_path, 'r') as file:  # Read chosen file
                data = file.readlines()
                for i, line in enumerate(data):
                    if i == len(data) - 1:  # Check for
                        self.input_connection(self, line.replace('\n', ''), True)
                    else:
                        self.input_connection(self, line.replace('\n', ''))

    def input_connection(self, var, file_var=None, last=None):
        try:
            if not file_var:
                var = list(map(int, var))
            else:
                var = list(map(int, file_var.split()))
        except ValueError:
            var = None
        if not var:
            make_new_window('Не все введенные являются числами!')
        elif len(var) != 3:
            make_new_window('Введенные данные должны состоять из трех чисел!')
        elif var[0] == var[1]:
            make_new_window('В графе не должно быть петель!')
        else:
            checked, already_exist = self.info.connection_check(var)
            if already_exist:
                make_new_window('Вы ввели связь, которая уже существовала!\nСначала удалите старую связь!')
            else:
                if not checked:  # Connection doesn't exist and we insert this connection
                    self.insert_connection(var, last, file_var)
                else:  # Connection exist and we delete this connection
                    self.delete_connection(var)
        # else:
        #     make_new_window('В полученных данных есть ошибки!\nНекорректные данные были удалены из списка\n'
        #                     'Вы можете очистить эти данные или продолжить работать с ними')

    def insert_connection(self, var, last, file_var=None):
        self.info.insert_connection(var)
        if last:
            new_info = ''
            for line in self.info.get_connections():
                new_info += ' '.join(str(x) for x in line) + '\n'
            self.view.change_input_info_scrl_label(new_info)
            self.view.change_vertex_count_label(self.info.get_vertexes_count())
        if not file_var:
            self.view.change_input_info_scrl_label(' '.join(str(x) for x in var) + '\n', True)
            self.view.change_vertex_count_label(self.info.get_vertexes_count())

    def delete_connection(self, var):
        self.info.delete_connection(var)
        new_info = ''
        for line in self.info.get_connections():
            new_info += ' '.join(str(x) for x in line) + '\n'
        self.view.change_input_info_scrl_label(new_info)
        self.view.change_vertex_count_label(self.info.get_vertexes_count())

    def input_src(self, src):
        try:
            src = int(src)
            if src in self.info.get_vertexes():
                self.info.insert_src(src)
                self.view.change_src_entry(src)
            else:
                make_new_window('Данной вершины нет в графе!')
        except ValueError:
            make_new_window('Данные введены неверно!')

    def _make_graph(self, wfi) -> tuple:
        draw = self.view.draw_switch.get()
        g = Graph(self.info.get_vertexes_count())
        for line in self.info.get_connections():
            g.add_edge(line[0], line[1], line[2])
        if not wfi:
            return g.spfa(int(self.info.get_src()), draw)
        else:
            return g.wfi(draw)

    def clear(self):
        self.info.clear()
        self.view.clear()


if __name__ == '__main__':
    back = Back(View(), Info())
    cProfile.run('back.start()', sort='cumtime')
