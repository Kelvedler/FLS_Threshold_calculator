from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3

root = Tk()
root.title("FLS Threshold Calculator")
root.geometry("1267x692")

frame = LabelFrame(root, padx=5, pady=5)
frame.grid(row=0, column=0, padx=10, pady=10)

fls_active = 2
input_info = []
graph_active = Label(frame)
graph_active.grid(row=0, column=0, padx=20, pady=20)

input_label = Label()

heading_text = ("Registration\nNumber",
                "Flight Hours\n ",
                "Flight Cycles\n ",
                "Flight Hours\nDaily",
                "Flight Cycles\nDaily",
                "Figure 1\nDue Date",
                "Figure 2\nDue Date")


def ac_table():
    db_conn = sqlite3.connect("AC data")
    db_cursor = db_conn.cursor()
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS acData (
        reg_num TEXT PRIMARY KEY,
        flight_h REAL,
        flight_c REAL,
        flight_h_daily REAL,
        flight_c_daily REAL,
        f_c_th_75x100 REAL,
        f_c_th_56x75 REAL
    )""")
    db_conn.commit()
    db_conn.close()


class InputBox(LabelFrame):

    def __init__(self):
        super().__init__(root, padx=5, pady=5)
        self.grid(row=1, column=0, padx=10, pady=10, sticky=EW)

        reg_n_len = StringVar()
        fl_h_len = StringVar()
        fl_c_len = StringVar()
        fl_h_d_len = StringVar()
        fl_c_d_len = StringVar()

        Label(self, text=heading_text[0]).grid(row=0, column=0)
        reg_num = Entry(self, width=10, textvariable=reg_n_len)
        reg_n_len.trace("w", lambda *args: self.entry_limit(reg_n_len))
        reg_num.grid(row=1, column=0)
        self.reg_num = reg_num

        Label(self, text=heading_text[1]).grid(row=0, column=1)
        flight_h = Entry(self, validate="key", width=10, textvariable=fl_h_len)
        fl_h_len.trace("w", lambda *args: self.entry_limit(fl_h_len))
        flight_h.configure(validatecommand=(flight_h.register(self.val_int), '%P', '%d'))
        flight_h.grid(row=1, column=1)
        self.flight_h = flight_h

        Label(self, text=heading_text[2]).grid(row=0, column=2)
        flight_c = Entry(self, validate="key", width=10, textvariable=fl_c_len)
        fl_c_len.trace("w", lambda *args: self.entry_limit(fl_c_len))
        flight_c.configure(validatecommand=(flight_c.register(self.val_int), '%P', '%d'))
        flight_c.grid(row=1, column=2)
        self.flight_c = flight_c

        Label(self, text=heading_text[3]).grid(row=0, column=3)
        flight_h_daily = Entry(self, validate="key", width=10, textvariable=fl_h_d_len)
        fl_h_d_len.trace("w", lambda *args: self.entry_limit(fl_h_d_len))
        flight_h_daily.configure(validatecommand=(flight_h_daily.register(self.val_int), '%P', '%d'))
        flight_h_daily.grid(row=1, column=3)
        self.flight_h_daily = flight_h_daily

        Label(self, text=heading_text[4]).grid(row=0, column=4)
        flight_c_daily = Entry(self, validate="key", width=10, textvariable=fl_c_d_len)
        fl_c_d_len.trace("w", lambda *args: self.entry_limit(fl_c_d_len))
        flight_c_daily.configure(validatecommand=(flight_c_daily.register(self.val_int), '%P', '%d'))
        flight_c_daily.grid(row=1, column=4)
        self.flight_c_daily = flight_c_daily

        save_btn = Button(self, text="Save", command=self.save_info, width=12)
        save_btn.grid(row=1, column=5)
        self.save_btn = save_btn

        draw_btn = Button(self, text="Draw", command=self.draw_graph, width=12)
        draw_btn.grid(row=1, column=6)
        self.draw_btn = draw_btn

    @staticmethod
    def entry_limit(sv):
        c = sv.get()[0:7]
        sv.set(c)

    @staticmethod
    def val_int(input_str, char_name):
        if char_name == "1":
            if not input_str.replace(".", "", 1).isdigit():
                return False
        return True

    def data_check(self, button):
        data_status = ""
        global input_label
        input_label.grid_forget()
        if self.flight_h.get() == "" or \
                self.flight_h_daily.get() == "" or \
                self.flight_c_daily.get() == "":
            data_status = "Please,\n fill all fields"
            check = False
        else:
            if self.reg_num.get() == "" and button == "save":
                data_status = "Please,\n fill all fields"
                check = False
            else:
                if button == "save":
                    data_status = "Saved"
                check = True
        input_label = Label(self, text=data_status, fg="red")
        input_label.grid(row=0, column=5)
        return check

    def save_info(self):
        if self.data_check("save"):
            ac_reg = str(self.reg_num.get())
            global input_info
            input_info = [float(self.flight_h.get()),
                          float(self.flight_c.get()),
                          float(self.flight_h_daily.get()),
                          float(self.flight_c_daily.get())]
            f_c_th_75x100 = intersection_point("75x100")[1]
            f_c_th_56x75 = intersection_point("56x75")[1]
            db_conn = sqlite3.connect("AC data")
            db_cursor = db_conn.cursor()
            db_cursor.execute(f"""INSERT INTO acData VALUES (
                            '{ac_reg}',
                            '{input_info[0]}',
                            '{input_info[1]}',
                            '{input_info[2]}',
                            '{input_info[3]}',
                            '{f_c_th_75x100}',
                            '{f_c_th_56x75}'
                )""")
            db_conn.commit()
            db_conn.close()
            ac_box.display_ac()

    def draw_graph(self):
        if self.data_check("draw"):
            global input_info
            input_info = [float(self.flight_h.get()),
                          float(self.flight_c.get()),
                          float(self.flight_h_daily.get()),
                          float(self.flight_c_daily.get())]
            graph_background_create()

    def insert_from_treev(self, r_n_new, f_h_new, f_c_new, f_h_d_new, f_c_d_new):
        self.reg_num.delete(0, END)
        self.flight_h.delete(0, END)
        self.flight_c.delete(0, END)
        self.flight_h_daily.delete(0, END)
        self.flight_c_daily.delete(0, END)

        self.reg_num.insert(0, r_n_new)
        self.flight_h.insert(0, f_h_new)
        self.flight_c.insert(0, f_c_new)
        self.flight_h_daily.insert(0, f_h_d_new)
        self.flight_c_daily.insert(0, f_c_d_new)


def intersection_point(graph):
    fl_h, fl_c, fl_h_d, fl_c_d = input_info
    floating_line = ((fl_h, fl_c), (fl_h + fl_h_d, fl_c + fl_c_d))

    def intersection_calc(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    if graph == "75x100":
        threshold_lines = [((0, 75000), (45000, 75000)),
                           ((45000, 75000), (100000, 30000)),
                           ((100000, 30000), (100000, 0))]
    else:
        threshold_lines = [((0, 56000), (33000, 56000)),
                           ((33000, 56000), (75000, 22000)),
                           ((75000, 22000), (75000, 0))]

    control_point = (intersection_calc(floating_line, threshold_lines[1]))
    if control_point[0] > threshold_lines[1][1][0]:
        intersection = (intersection_calc(floating_line, threshold_lines[2]))
    elif control_point[1] > threshold_lines[0][0][1]:
        intersection = (intersection_calc(floating_line, threshold_lines[0]))
    else:
        intersection = control_point
    intersection = round(intersection[0], 2), round(intersection[1], 2)
    return intersection


def graph_background_create():
    global graph_active
    fl_h_int = 0
    fl_c_int = 0
    if fls_active == 1:
        graph_75x100 = Figure(figsize=(6, 5), dpi=100)
        plot = graph_75x100.add_subplot(111)
        plot.plot([0, 45000, 100000, 100000], [75000, 75000, 30000, 0], "-k")
        if input_info:
            fl_h_int, fl_c_int = intersection_point("75x100")
            plot.plot([input_info[0], fl_h_int], [input_info[1], fl_c_int], "-r")

        graph_active = FigureCanvasTkAgg(graph_75x100, master=frame)
        graph_active.draw()
    else:
        graph_56x75 = Figure(figsize=(6, 5), dpi=100)
        plot = graph_56x75.add_subplot(111)
        plot.plot([0, 33000, 75000, 75000], [56000, 56000, 22000, 0], "-k")
        if input_info:
            fl_h_int, fl_c_int = intersection_point("56x75")
            plot.plot([input_info[0], fl_h_int], [input_info[1], fl_c_int], "-r")

        graph_active = FigureCanvasTkAgg(graph_56x75, master=frame)
        graph_active.draw()
    graph_active.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, columnspan=4)
    display_threshold(fl_h_int, fl_c_int)


def display_threshold(fh, fc):
    fh = str(fh)
    fc = str(fc)
    threshold = Label(frame, text=fh + " FH " + fc + " FC", width=18)
    threshold.grid(row=1, column=3)


def graph_switch():
    global fls_active
    if fls_active == 2:
        fls_active = 1
    else:
        fls_active = 2
    print(root.winfo_width())  # TODO Delete This Line
    print(root.winfo_height())  # TODO Delete This Line
    graph_background_create()


class AcBox(LabelFrame):

    def __init__(self):
        super().__init__(master=root, padx=5, pady=5)
        self.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky=NS)
        treev = ttk.Treeview(self, selectmode='browse', height=31)
        treev_columns = ("1", "2", "3", "4", "5", "6", "7")
        treev["columns"] = treev_columns
        treev["show"] = "headings"
        for column in treev_columns:
            treev.column(column, width=75)
            treev.heading(column, text=heading_text[int(column) - 1])
        treev.grid(row=0, column=1)

        ac_box_scroll = ttk.Scrollbar(self, orient=VERTICAL, command=treev.yview)
        ac_box_scroll.grid(row=0, column=0, sticky=NS)
        treev['yscrollcommand'] = ac_box_scroll.set
        treev.bind('<<TreeviewSelect>>', self.treev_callback)
        self.treev = treev

    def display_ac(self):
        for record in self.treev.get_children():
            self.treev.delete(record)
        db_conn = sqlite3.connect("AC data")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * FROM acData")
        ac_data_list = db_cursor.fetchall()
        db_conn.commit()
        db_conn.close()
        l_var = 0
        for aircraft in ac_data_list:
            reg_num, flight_h, flight_c, flight_h_daily, flight_c_daily, f_c_th_75x100, f_c_th_56x75 = aircraft
            self.treev.insert("", "end", iid=l_var, values=(
                reg_num, flight_h, flight_c, flight_h_daily, flight_c_daily, f_c_th_75x100, f_c_th_56x75))
            l_var += 1

    def treev_callback(self, _):
        treev_id = self.treev.selection()[0]
        reg_num, flight_h, flight_c, flight_h_daily, flight_c_daily, _, _ = self.treev.item(treev_id)["values"]
        input_box.insert_from_treev(reg_num, flight_h, flight_c, flight_h_daily, flight_c_daily)
        input_box.draw_graph()


graph_background_create()

input_box = InputBox()

ac_table()
ac_box = AcBox()
ac_box.display_ac()

graph_switch_btn = Button(frame, text="Change Graph", width=12, command=graph_switch)
graph_switch_btn.grid(row=1, column=2)

root.mainloop()
