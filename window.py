import random
import tkinter
import tkinter as tk

import matplotlib.pyplot as plt
import names
from pandas import DataFrame


class window:

    def __init__(self, data):
        self.info_table_dict = {}
        self.info_table_vars = {}
        self.rows = len(data)
        self.columns = len(data[0])
        self.data = data
        self.canvas = None
        self.x_var_option_value = None
        self.y_var_option_value = None

        self.set_up_widgets()

    def plot(self, title='Year Vs. Unemployment Rate'):
        if self.data is None:
            raise Exception("please input data before using window.plot")
        figure = plt.figure()
        ax2 = figure.add_subplot(111)
        data_dict = {self.data[0][i]:[self.data[x][i] for x in range(1,len(self.data))] for i in range(0,len(self.data[0]))}
        print(data_dict)
        data2 = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
                 'Unemployment_Rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
                 }
        df2 = DataFrame(data_dict, columns=['roll_no'])
        df2 = df2['roll_no'].value_counts()
        df2.plot(kind='bar')
        ax2.set_title(title)
        plt.show()

    def set_data(self, data):
        r = 0
        self.data = data.copy()

        while r < self.rows and r < len(data):
            for c in range(len(data[r])):
                if self.columns - 1 >= c:
                    self.info_table_vars[(r, c)].set(str(data[r][c]))
            r += 1

    def set_up_widgets(self):
        # setting up root
        root = tk.Tk(className=" GRAPHICAL DATA VISUALISER")
        root.geometry("1200x600")
        root.resizable(False, False)

        # table frame
        table_and_options_frame = tk.Frame(root, height=600, width=800)
        table_and_options_frame.pack(side=tk.LEFT)
        table_and_options_frame.grid_propagate(0)

        # graph viewer frame
        graph_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, height=600, width=400)
        graph_frame.pack(side=tk.RIGHT)
        graph_frame.grid_propagate(0)

        # setting up table
        outer_table_frame = tk.Frame(table_and_options_frame, height=400, width=800)
        outer_table_frame.grid(row=0, column=0, sticky=tk.NW)

        # adding canvas
        canvas = tk.Canvas(outer_table_frame, bg="white")
        canvas.grid(row=0, column=0)
        self.canvas = canvas

        # Create a vertical scrollbar linked to the canvas.

        vsbar = tk.Scrollbar(outer_table_frame, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(outer_table_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)

        canvas.configure(xscrollcommand=hsbar.set)

        table_frame = tk.Frame(canvas, bd=2)

        for r in range(self.rows):
            for c in range(self.columns):
                if r == 0:
                    # info = info_List[(r, c)]
                    # info = [image,name,price, ]
                    self.info_table_vars[(r, c)] = tk.StringVar()
                    self.info_table_dict[(r, c)] = [
                        tk.Entry(table_frame, width=14, font=('Arial', 10, 'bold'), fg='black',
                                 textvariable=self.info_table_vars[(r, c)])]

                    self.info_table_dict[(r, c)][0].grid(row=r, column=c, sticky='news')
                else:
                    self.info_table_vars[(r, c)] = tk.StringVar()
                    self.info_table_dict[(r, c)] = [
                        tk.Entry(table_frame, width=14, font=('Arial', 10, 'bold'), fg='blue',
                                 textvariable=self.info_table_vars[(r, c)])]
                    self.info_table_dict[(r, c)][0].grid(row=r, column=c, sticky='news')
                    # self.info_table_vars[(r, c)].set('R%s/C%s' % (r, c))

        canvas.create_window((0, 0), window=table_frame, anchor=tk.NW)
        table_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with entries.
        canvas.configure(scrollregion=bbox, width=780, height=380)

        # table options
        save_data = tk.Button(table_and_options_frame, text="save data", command=self.save_data,
                              font=('Arial', 16, 'bold'), width=15, bd=4)
        save_data.place(x=600, y=550, height=50, width=200)

        reset_data = tk.Button(table_and_options_frame, text="reset data", command=self.reset_data,
                               font=('Arial', 16, 'bold'), width=15, bd=4)
        reset_data.place(x=600, y=500, height=50, width=200)

        button_dynamic = tk.Button(table_and_options_frame, text="DYNAMIC LENGTH ADJUST",
                                   command=self.dynamic_length_adjust, width=25,
                                   font=('Arial', 10, 'bold'), bd=4)
        button_dynamic.place(x=600, y=450, height=50, width=200)

        # sets data here as all of the table is set up

        self.set_data(self.data)

        # graph viewer frame

        # TOP LABEL : GRAPH OPTIONS
        graph_label = tk.Label(graph_frame, text="GRAPH OPTIONS", justify=tk.CENTER, font=('Arial', 20, 'bold'),
                               width=24, relief=tk.GROOVE)
        graph_label.grid(row=0, column=0, columnspan=4)

        # SHOW / DELETE  GRAPH BUTTON

        def toggle(toggle_btn):
            if toggle_btn.config('relief')[-1] == 'sunken':
                toggle_btn.config(relief="raised")
                toggle_btn['state'] = "normal"
            else:
                toggle_btn.config(relief="sunken")
                toggle_btn["state"] = "disabled"

        def show_graph():

            toggle(button_show_graph)
            toggle(button_delete_graph)
            print(graph_name_var.get())
            self.plot(graph_name_var.get())

        def delete_graph():

            toggle(button_show_graph)
            toggle(button_delete_graph)
            plt.close()

        button_show_graph = tk.Button(graph_frame, text="SHOW GRAPH", command=show_graph, width=15,
                                      font=('Arial', 16, 'bold'), bd=4)

        button_delete_graph = tk.Button(graph_frame, text="DELETE GRAPH", command=delete_graph, width=15,
                                        relief="sunken", font=('Arial', 16, 'bold'), bd=4, state='disabled')

        button_show_graph.place(x=0, y=550, height=50, width=200, anchor=tk.NW)

        button_delete_graph.place(x=200, y=550, height=50, width=200, anchor=tk.NW)

        # graph name entry

        label_graph_name = tk.Label(graph_frame, text="NAME OF GRAPH :", font=('Arial', 12, 'bold'), justify=tk.CENTER)
        label_graph_name.place(x=10, y=50, width=150, height=40)
        graph_name_var = tk.StringVar(value="Year Vs. Unemployment Rate")

        entry_graph_name = tk.Entry(graph_frame, textvariable=graph_name_var, font=('Arial', 12, 'bold'), bd=" 2",
                                    relief="groove")
        entry_graph_name.place(x=160, y=50, width=230, height=40)

        # graph functions
        x_var_label = tk.Label(graph_frame, text=" x =", justify=tk.CENTER, font=('Arial', 20, 'bold'),
                               width=5)
        x_var_label.place(x=10, y=100, width=50, height=40)
        self.x_var_option_value = tk.StringVar()

        x_var_option = tkinter.OptionMenu(graph_frame, self.x_var_option_value, *self.data[0], "custom")
        x_var_option.place(x=80, y=100, width=150, height=40)
        self.x_var_option_value.set("choose option")

        # x var functions

        y_var_label = tk.Label(graph_frame, text=" y =", justify=tk.CENTER, font=('Arial', 20, 'bold'),
                               width=5)
        y_var_label.place(x=10, y=300, width=50, height=40)
        self.y_var_option_value = tk.StringVar()

        y_var_option = tkinter.OptionMenu(graph_frame, self.y_var_option_value, 'frequency', "custom")
        y_var_option.place(x=80, y=300, width=150, height=40)
        self.y_var_option_value.set("choose option")



    def save_data(self):
        new_data = [self.data[0].copy()]
        for r in range(1, self.rows):
            row = []
            for c in range(self.columns):
                row.append(self.info_table_vars[(r, c)].get())
            new_data.append(row)

        self.data = new_data.copy()

    def reset_data(self):
        r = 0

        while r < self.rows and r < len(self.data):
            for c in range(len(self.data[r])):
                if self.columns - 1 >= c:
                    self.info_table_vars[(r, c)].set(str(self.data[r][c]))
            r += 1

    def dynamic_length_adjust(self):
        length_of_columns = list()

        def column(arr_2d, i):
            return [row[i] for row in arr_2d]

        for c in range(len(self.data[0])):
            length_of_columns.append([len(str(x)) for x in column(self.data, c)])

        max_len_columns = [max(x) + 1 for x in length_of_columns]
        for r in range(self.rows):
            for c in range(self.columns):
                self.info_table_dict[(r, c)][0].configure(width=max_len_columns[c])
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def swap_column(self, column1_no, column2_no):

        if not column1_no == column2_no:
            for (r, c), var in self.info_table_vars.items():
                if c == column1_no:
                    var1 = self.info_table_vars[(r, c)].get()
                    var2 = self.info_table_vars[(r, column2_no)].get()
                    self.info_table_vars[(r, c)].set(var2)
                    self.info_table_vars[(r, column2_no)].set(var1)
        # self.dynamic_length_adjust()

    def swap_row(self, row1_no, row2_no):

        if not row1_no == row2_no:
            for (r, c), var in self.info_table_vars.items():
                if r == row1_no:
                    var1 = self.info_table_vars[(r, c)].get()
                    var2 = self.info_table_vars[(row2_no, c)].get()
                    self.info_table_vars[(r, c)].set(var2)
                    self.info_table_vars[(row2_no, c)].set(var1)
        # self.dynamic_length_adjust()


if __name__ == '__main__':
    def gen_data():
        data_row = [random.randint(0, 100), random.randint(0, 100), names.get_full_name(), random.randint(0, 10000),
                    random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                    random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                    random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                    random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]

        return data_row


    database = [['no', 'age', 'name', 'roll_no', *[f"column_{4 + x}" for x in range(16)]],
                *[gen_data() for _ in range(100)]]
    app = window(database)

    # app.dynamic_length_adjust()

    tk.mainloop()
