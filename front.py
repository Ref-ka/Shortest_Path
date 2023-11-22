import time

import customtkinter as tk
from make_graph import make_graph
from PIL import Image
from os import remove, path
from info_class import Info
from tkinter import filedialog

info = Info()

window = tk.CTk()
window.geometry('1299x850')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(2, weight=1)
window.minsize(1299, 850)


# Команда ввода

def input_connection_command(file_var=None):
    try:
        if not file_var:
            var = list(map(int, input_entry.get().split()))
        else:
            var = list(map(int, file_var.split()))
    except ValueError:
        make_new_window('Введенные или загруженные\nданные неверны!')
        var = None
    finally:
        pass
    start_insert = time.monotonic()
    if var and len(var) == 3:
        if var[0] != var[1]:
            if not info.connection_check(var):
                info.insert_connection(var)
                input_info_scrl.configure(text=input_info_scrl.cget('text') + ' '.join(str(x) for x in var) + '\n')
                if not file_var:
                    input_entry.delete(0, 'end')
            else:
                info.delete_connection(var)
                new_info = ''
                for line in info.get_connections():
                    new_info += ' '.join(str(x) for x in line) + '\n'
                input_info_scrl.configure(text=new_info)
                if not file_var:
                    input_entry.delete(0, 'end')
    print(f'insert_time {time.monotonic() - start_insert}')
    vertex_count_info_label.configure(text=f'Количество вершин:\n{info.get_vertexes_count()}')


def input_src_command():
    try:
        src = int(src_entry.get())
        if src in info.vertexes:
            info.insert_src(src_entry.get())
            src_entry.delete(0, 'end')
            src_info_label.configure(text=f'Начальная вершина:\n{str(info.get_src())}')
    except ValueError:
        make_new_window('Данные введены неверно!')


# Команда получения ответа

def get_answer(wfi=False):
    if (info.get_connections() and info.get_src()) or (info.get_connections() and wfi):

        if path.exists('graph.png'):
            remove('graph.png')

        ans, history, buf = make_graph(info.get_vertexes_count(), info.get_connections(), info.get_src(), wfi)

        output_textbox_1.configure(state='normal')
        output_textbox_2.configure(state='normal')

        output_textbox_1.delete('0.0', 'end')
        output_textbox_2.delete('0.0', 'end')

        if ans.empty:
            ans = 'В графе есть\nотрицательный цикл!'
        elif not wfi:
            ans = ans.T

        output_textbox_1.insert('0.0', ans)

        output_textbox_2.insert('0.0', history)

        output_textbox_1.configure(state='disable')
        output_textbox_2.configure(state='disable')
        start_load = time.monotonic()
        image = tk.CTkImage(dark_image=Image.open(buf), size=(700, 620))
        image_label.configure(image=image)
        print(f'load_time {time.monotonic() - start_load}')
    else:
        make_new_window('Вы не ввели некоторые данные!\n''Проверьте все колонки ввода!')


def get_answer_wfi():
    get_answer(True)


def make_new_window(text):
    problem_window = tk.CTkToplevel()
    problem_window.geometry('300x100')
    problem_window.grab_set()
    problem_label = tk.CTkLabel(problem_window, font=tk.CTkFont('Gill Sans', 13, weight='bold'), text=text)
    problem_label.pack(pady=20)


def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        clear()
        start_input = time.monotonic()
        with open(file_path, 'r') as file:
            for line in file.readlines():
                input_connection_command(line.replace('\n', ''))
        print(f'input_time {time.monotonic() - start_input}')


def clear():
    info.clear()
    input_info_scrl.configure(text='')
    src_info_label.configure(text='Начальная вершина:\n')
    vertex_count_info_label.configure(text='Количество вершин:\n')
    output_textbox_1.configure(state='normal')
    output_textbox_2.configure(state='normal')
    output_textbox_1.delete('0.0', 'end')
    output_textbox_2.delete('0.0', 'end')
    output_textbox_1.configure(state='disable')
    output_textbox_2.configure(state='disable')
    image_label.configure(image=None)


# Frames
# region
input_frame = tk.CTkFrame(window, fg_color='#C2C2C2', height=100, border_color='#151E3D',
                          border_width=3)
graph_vis_frame = tk.CTkFrame(window, fg_color='white', height=600, width=700)  # border_color='#151E3D', border_width=3
output_frame = tk.CTkFrame(window, fg_color='#C2C2C2', height=768, width=288, border_color='#151E3D',
                           border_width=3)
input_info_scrl_frame = tk.CTkScrollableFrame(input_frame, fg_color='#DCDCDC', width=170, height=280)
output_subframe_1 = tk.CTkFrame(output_frame, height=281, fg_color='#C2C2C2')
output_subframe_2 = tk.CTkFrame(output_frame, height=281, fg_color='#C2C2C2')
output_subframe_3 = tk.CTkFrame(output_frame, height=206, fg_color='#C2C2C2')

input_frame.grid_columnconfigure(0, weight=1)
graph_vis_frame.grid_columnconfigure(0, weight=1)
graph_vis_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

output_subframe_1.grid(row=0, pady=5)
output_subframe_2.grid(row=1, pady=5)
output_subframe_3.grid(row=2, pady=5)

input_frame.grid(row=0, column=0, sticky='EWNS')
graph_vis_frame.grid(row=0, column=1, rowspan=3, sticky='EWNS')
output_frame.grid(row=0, column=2, rowspan=3, sticky='EWNS')
input_info_scrl_frame.grid(row=1, column=0, padx=4)

output_frame.grid_propagate(False)
graph_vis_frame.grid_propagate(False)
# endregion

# Buttons
# region
input_connection_button = tk.CTkButton(input_frame, text='Ввод', command=input_connection_command, fg_color='#29BCFF',
                                       text_color='#151E3D',
                                       font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
input_src_button = tk.CTkButton(input_frame, text='Ввод', command=input_src_command, fg_color='#29BCFF',
                                text_color='#151E3D',
                                font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
ans_button = tk.CTkButton(input_frame, text='Рассчитать по spfa', command=get_answer, fg_color='#29BCFF',
                          text_color='#151E3D', font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
file_button = tk.CTkButton(output_subframe_3, text='Выбрать файл', command=load_file, fg_color='#29BCFF',
                           text_color='#151E3D',
                           font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
clear_button = tk.CTkButton(output_subframe_3, text='Очистить всё', command=clear, fg_color='#29BCFF',
                            text_color='#151E3D',
                            font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
wfi_button = tk.CTkButton(input_frame, text='Рассчитать по wfi', command=get_answer_wfi, fg_color='#29BCFF',
                          text_color='#151E3D',
                          font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')

input_connection_button.grid(row=6, column=0, padx=30)
input_src_button.grid(row=9, padx=30)
ans_button.grid(row=10, pady=30)
file_button.grid(row=1, pady=10)
clear_button.grid(row=2, pady=10)
wfi_button.grid(row=11)
# endregion

# Entry
# region
input_entry = tk.CTkEntry(input_frame, fg_color='#DCDCDC', text_color='#151E3D')
src_entry = tk.CTkEntry(input_frame, fg_color='#DCDCDC', text_color='#151E3D')

input_entry.grid(row=5, column=0, padx=30)
src_entry.grid(row=8)
# endregion

# Label
# region
input_info_label = tk.CTkLabel(input_frame, text='Здесь будет\nвведенная информация',
                               font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
input_info_scrl = tk.CTkLabel(input_info_scrl_frame, text='',
                              font=tk.CTkFont('Courier New', 17, weight='bold'), text_color='#151E3D')
output_label_1 = tk.CTkLabel(output_subframe_1, text='     Здесь будет ответ     ',
                             font=tk.CTkFont('Gill Sans', 17, weight='bold'), text_color='#151E3D')
entry_label = tk.CTkLabel(input_frame, text='Ввод вершин и весов',
                          font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
src_label = tk.CTkLabel(input_frame, text='Ввод\nначальной вершины',
                        font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
image_label = tk.CTkLabel(graph_vis_frame, text='', height=768, width=812)
src_info_label = tk.CTkLabel(input_frame, text='Начальная вершина:\n',
                             font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
vertex_count_info_label = tk.CTkLabel(input_frame, text='Количество вершин:\n',
                                      font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
output_label_2 = tk.CTkLabel(output_subframe_2, text='Здесь будут шаги\nвыполнения алгоритма',
                             font=tk.CTkFont('Gill Sans', 17, weight='bold'), text_color='#151E3D')

input_info_label.grid(row=0, column=0, pady=10)
output_label_1.grid(row=0, column=0, padx=30, pady=10, sticky='EWNS')
input_info_scrl.grid(padx=20, pady=10)
entry_label.grid(row=4, pady=10)
src_label.grid(row=7, pady=10)
image_label.grid(row=0, pady=10, padx=10)
src_info_label.grid(row=2, pady=10)
vertex_count_info_label.grid(row=3, pady=10)
output_label_2.grid(row=0, column=0, padx=30, pady=10, sticky='EWNS')
# endregion

# Textbox
output_textbox_1 = tk.CTkTextbox(output_subframe_1, wrap='none', font=tk.CTkFont('Courier New', 17, weight='bold'),
                                 width=300, state='disable', fg_color='#DCDCDC', text_color='#151E3D', height=300)
output_textbox_2 = tk.CTkTextbox(output_subframe_2, wrap='none', font=tk.CTkFont('Courier New', 17, weight='bold'),
                                 width=300, state='disable', fg_color='#DCDCDC', text_color='#151E3D', height=300)

output_textbox_1.grid_propagate(False)
output_textbox_2.grid_propagate(False)

output_textbox_1.grid()
output_textbox_2.grid()


window.mainloop()
