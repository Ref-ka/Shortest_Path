import customtkinter as tk
from PIL import Image


def make_new_window(text):
    problem_window = tk.CTkToplevel()
    problem_window.geometry('450x100')
    problem_window.grab_set()
    problem_label = tk.CTkLabel(problem_window, font=tk.CTkFont('Gill Sans', 13, weight='bold'), text=text)
    problem_label.pack(pady=20)


class View:
    def setup(self, back):
        self.window = tk.CTk()
        self.window.geometry('1299x850')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.minsize(1299, 850)

        # Frames
        # region
        input_frame = tk.CTkFrame(self.window, fg_color='#C2C2C2', height=100, border_color='#151E3D',
                                  border_width=3)
        graph_vis_frame = tk.CTkFrame(self.window, fg_color='white', height=600, width=700)
        output_frame = tk.CTkFrame(self.window, fg_color='#C2C2C2', height=768, width=288, border_color='#151E3D',
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
        input_connection_button = tk.CTkButton(input_frame, text='Ввод',
                                               command=lambda:
                                               back.input_connection_command(self.input_entry.get().split()),
                                               fg_color='#29BCFF',
                                               text_color='#151E3D',
                                               font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
        input_src_button = tk.CTkButton(input_frame, text='Ввод',
                                        command=lambda: back.input_src_command(self.src_entry.get()),
                                        fg_color='#29BCFF',
                                        text_color='#151E3D',
                                        font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
        spfa_button = tk.CTkButton(input_frame, text='Рассчитать по spfa',
                                   command=lambda: back.get_answer(), fg_color='#29BCFF',
                                   text_color='#151E3D', font=tk.CTkFont('Gill Sans', 13, weight='bold'),
                                   hover_color='#1CA1DF')
        file_button = tk.CTkButton(output_subframe_3, text='Выбрать файл', command=back.load_file, fg_color='#29BCFF',
                                   text_color='#151E3D',
                                   font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
        clear_button = tk.CTkButton(output_subframe_3, text='Очистить всё', command=back.clear, fg_color='#29BCFF',
                                    text_color='#151E3D',
                                    font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')
        wfi_button = tk.CTkButton(input_frame, text='Рассчитать по wfi',
                                  command=lambda: back.get_answer(True), fg_color='#29BCFF',
                                  text_color='#151E3D',
                                  font=tk.CTkFont('Gill Sans', 13, weight='bold'), hover_color='#1CA1DF')

        input_connection_button.grid(row=6, column=0, padx=30)
        input_src_button.grid(row=9, padx=30)
        spfa_button.grid(row=10, pady=30)
        file_button.grid(row=1, pady=10)
        clear_button.grid(row=2, pady=10)
        wfi_button.grid(row=11)
        # endregion

        # Entry
        # region
        self.input_entry = tk.CTkEntry(input_frame, fg_color='#DCDCDC', text_color='#151E3D')
        self.src_entry = tk.CTkEntry(input_frame, fg_color='#DCDCDC', text_color='#151E3D')

        self.input_entry.grid(row=5, column=0, padx=30)
        self.src_entry.grid(row=8)
        # endregion

        # Label
        # region
        input_info_label = tk.CTkLabel(input_frame, text='Здесь будет\nвведенная информация',
                                       font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
        self.input_info_scrl_label = tk.CTkLabel(input_info_scrl_frame, text='',
                                                 font=tk.CTkFont('Courier New', 17, weight='bold'),
                                                 text_color='#151E3D')
        output_label_1 = tk.CTkLabel(output_subframe_1, text='     Здесь будет ответ     ',
                                     font=tk.CTkFont('Gill Sans', 17, weight='bold'), text_color='#151E3D')
        entry_label = tk.CTkLabel(input_frame, text='Ввод вершин и весов',
                                  font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
        src_label = tk.CTkLabel(input_frame, text='Ввод\nначальной вершины',
                                font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
        self.image_label = tk.CTkLabel(graph_vis_frame, text='', height=768, width=812)
        self.src_info_label = tk.CTkLabel(input_frame, text='Начальная вершина:\n',
                                          font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
        self.vertex_count_label = tk.CTkLabel(input_frame, text='Количество вершин:\n',
                                              font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D')
        output_label_2 = tk.CTkLabel(output_subframe_2, text='Здесь будут шаги\nвыполнения алгоритма',
                                     font=tk.CTkFont('Gill Sans', 17, weight='bold'), text_color='#151E3D')

        input_info_label.grid(row=0, column=0, pady=10)
        output_label_1.grid(row=0, column=0, padx=30, pady=10, sticky='EWNS')
        self.input_info_scrl_label.grid(padx=20, pady=10)
        entry_label.grid(row=4, pady=10)
        src_label.grid(row=7, pady=10)
        self.image_label.grid(row=0, pady=10, padx=10)
        self.src_info_label.grid(row=2, pady=10)
        self.vertex_count_label.grid(row=3, pady=10)
        output_label_2.grid(row=0, column=0, padx=30, pady=10, sticky='EWNS')
        # endregion

        # Textbox
        self.output_textbox_1 = tk.CTkTextbox(output_subframe_1, wrap='none',
                                              font=tk.CTkFont('Courier New', 17, weight='bold'),
                                              width=300, state='disable',
                                              fg_color='#DCDCDC', text_color='#151E3D', height=300)
        self.output_textbox_2 = tk.CTkTextbox(output_subframe_2, wrap='none',
                                              font=tk.CTkFont('Courier New', 17, weight='bold'),
                                              width=300, state='disable',
                                              fg_color='#DCDCDC', text_color='#151E3D', height=300)

        self.output_textbox_1.grid_propagate(False)
        self.output_textbox_2.grid_propagate(False)

        self.output_textbox_1.grid()
        self.output_textbox_2.grid()

        # Switch
        self.draw_switch = tk.CTkSwitch(input_frame, text='Отключить отрисовку графа',
                                        font=tk.CTkFont('Gill Sans', 15, weight='bold'), text_color='#151E3D',
                                        progress_color='#29BCFF')

        self.draw_switch.grid(row=12, pady=7)

    def change_input_info_scrl_label(self, text, add=False):
        if add:
            self.input_info_scrl_label.configure(text=self.input_info_scrl_label.cget('text') + text)
        else:
            self.input_info_scrl_label.configure(text=text)
        self.input_entry.delete(0, 'end')

    def change_vertex_count_label(self, amount):
        self.vertex_count_label.configure(text=f'Количество вершин:\n{amount}')

    def change_src_entry(self, src):
        self.src_entry.delete(0, 'end')
        self.src_info_label.configure(text=f'Начальная вершина:\n{str(src)}')

    def show_answer(self, ans, history, buf, wfi):
        self.output_textbox_1.configure(state='normal')
        self.output_textbox_2.configure(state='normal')

        self.output_textbox_1.delete('0.0', 'end')
        self.output_textbox_2.delete('0.0', 'end')

        if ans.empty:
            ans = 'В графе есть\nотрицательный цикл!'
        elif not wfi:
            ans = ans.T

        self.output_textbox_1.insert('0.0', ans)

        self.output_textbox_2.insert('0.0', history)

        self.output_textbox_1.configure(state='disable')
        self.output_textbox_2.configure(state='disable')
        if buf:
            image = tk.CTkImage(dark_image=Image.open(buf), size=(700, 620))
            self.image_label.configure(image=image)

    def clear(self):
        self.input_info_scrl_label.configure(text='')
        self.src_info_label.configure(text='Начальная вершина:\n')
        self.vertex_count_label.configure(text='Количество вершин:\n')
        self.output_textbox_1.configure(state='normal')
        self.output_textbox_2.configure(state='normal')
        self.output_textbox_1.delete('0.0', 'end')
        self.output_textbox_2.delete('0.0', 'end')
        self.output_textbox_1.configure(state='disable')
        self.output_textbox_2.configure(state='disable')
        self.image_label.configure(image=None)

    def start_main_loop(self):
        self.window.mainloop()
