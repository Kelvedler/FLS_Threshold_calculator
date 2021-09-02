from tkinter import Label, Tk, StringVar, Entry, EW, END, NS, VERTICAL, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from functools import partial
import sqlite3

root = Tk()
root.title("FLS Threshold Calculator")
root.geometry("1390x676")
root.wm_maxsize(1390, 676)
root.wm_minsize(1390, 676)
root.iconbitmap("icon.ico")

root.call("source", "azure.tcl")
root.call("set_theme", "light")

frame = ttk.LabelFrame(root, padding=(5, 5))
frame.grid(row=0, column=0, padx=10)

fls_active = 2
input_info = []
graph_active = ttk.Label(frame)
graph_active.grid(row=0, column=0, padx=20, pady=20)

input_label = ttk.Label()

heading_text = ("Registration",
                "Flight Hours",
                "Flight Cycles",
                "FH Daily",
                "FC Daily",
                "Fig.1 Due Date",
                "Fig.2 Due Date")


class InputBox(ttk.LabelFrame):

    def __init__(self):
        super().__init__(root, padding=(5, 5))
        self.grid(row=1, column=0, padx=10, pady=10, sticky=EW)

        reg_n_len = StringVar()
        fl_h_len = StringVar()
        fl_c_len = StringVar()
        fl_h_d_len = StringVar()
        fl_c_d_len = StringVar()

        ttk.Label(self, text=heading_text[0]).grid(row=0, column=0, pady=2)
        reg_num = Entry(self, width=10, textvariable=reg_n_len)
        reg_n_len.trace("w", lambda *args: self.entry_limit(reg_n_len))
        reg_num.grid(row=1, column=0)
        self.reg_num = reg_num

        ttk.Label(self, text=heading_text[1]).grid(row=0, column=1, pady=2)
        flight_h = Entry(self, validate="key", width=10, textvariable=fl_h_len)
        fl_h_len.trace("w", lambda *args: self.entry_limit(fl_h_len))
        flight_h.configure(validatecommand=(flight_h.register(self.val_int), '%P', '%d'))
        flight_h.grid(row=1, column=1)
        self.flight_h = flight_h

        ttk.Label(self, text=heading_text[2]).grid(row=0, column=2, pady=2)
        flight_c = Entry(self, validate="key", width=10, textvariable=fl_c_len)
        fl_c_len.trace("w", lambda *args: self.entry_limit(fl_c_len))
        flight_c.configure(validatecommand=(flight_c.register(self.val_int), '%P', '%d'))
        flight_c.grid(row=1, column=2)
        self.flight_c = flight_c

        ttk.Label(self, text=heading_text[3]).grid(row=0, column=3, pady=2)
        flight_h_daily = Entry(self, validate="key", width=10, textvariable=fl_h_d_len)
        fl_h_d_len.trace("w", lambda *args: self.entry_limit(fl_h_d_len))
        flight_h_daily.configure(validatecommand=(flight_h_daily.register(self.val_int), '%P', '%d'))
        flight_h_daily.grid(row=1, column=3)
        self.flight_h_daily = flight_h_daily

        ttk.Label(self, text=heading_text[4]).grid(row=0, column=4, pady=2)
        flight_c_daily = Entry(self, validate="key", width=10, textvariable=fl_c_d_len)
        fl_c_d_len.trace("w", lambda *args: self.entry_limit(fl_c_d_len))
        flight_c_daily.configure(validatecommand=(flight_c_daily.register(self.val_int), '%P', '%d'))
        flight_c_daily.grid(row=1, column=4)
        self.flight_c_daily = flight_c_daily

        draw_btn = ttk.Button(self, text="Draw", command=self.draw_graph, width=9)
        draw_btn.grid(row=1, column=5, padx=3)
        self.draw_btn = draw_btn

        save_btn = ttk.Button(self, text="Save", command=self.save_info, width=9)
        save_btn.grid(row=1, column=6)
        self.save_btn = save_btn

        delete_btn = ttk.Button(self, text="Delete", command=self.delete_info, width=9)
        delete_btn.grid(row=1, column=7, padx=3)
        self.delete_btn = delete_btn

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
            data_status = "Please, fill all fields"
            check = False
        else:
            if self.reg_num.get() == "" and button == "save":
                data_status = "Please, fill all fields"
                check = False
            else:
                if button == "save":
                    data_status = "Saved"
                check = True
        input_label = ttk.Label(self, text=data_status, foreground="red")
        input_label.grid(row=0, column=5, columnspan=3)
        return check

    def save_info(self):
        if self.data_check("save"):
            ac_reg = str(self.reg_num.get())
            global input_info
            global input_label
            input_info = [float(self.flight_h.get()),
                          float(self.flight_c.get()),
                          float(self.flight_h_daily.get()),
                          float(self.flight_c_daily.get())]
            f_c_th_75x100 = intersection_point("75x100")[1]
            f_c_th_56x75 = intersection_point("56x75")[1]
            db_conn = sqlite3.connect("AC data")
            db_cursor = db_conn.cursor()
            if db_cursor.execute("SELECT reg_num FROM acData WHERE reg_num=?", (ac_reg,)).fetchone():
                db_cursor.execute(
                    """UPDATE acData SET 
                    flight_h=?, 
                    flight_c=?, 
                    flight_h_daily=?, 
                    flight_c_daily=?, 
                    f_c_th_75x100=?, 
                    f_c_th_56x75=? 
                    WHERE reg_num=?""",
                    (input_info[0], input_info[1], input_info[2], input_info[3], f_c_th_75x100, f_c_th_56x75, ac_reg))
                input_label.grid_forget()
                input_label = Label(self, text="Updated", fg="red")
                input_label.grid(row=0, column=5, columnspan=3)
            else:
                db_cursor.execute("INSERT INTO acData VALUES (?, ?, ?, ?, ?, ?, ? )", (
                    ac_reg, input_info[0], input_info[1], input_info[2], input_info[3], f_c_th_75x100, f_c_th_56x75))
            db_conn.commit()
            db_conn.close()
            ac_box.display_ac()

    def delete_info(self):
        ac_reg = str(self.reg_num.get())
        db_conn = sqlite3.connect("AC data")
        db_cursor = db_conn.cursor()
        db_cursor.execute("DELETE FROM acData WHERE reg_num=?", (ac_reg, ))
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
    graph_active.get_tk_widget().grid(row=0, column=0, padx=22, columnspan=8)
    display_threshold(fl_h_int, fl_c_int)


def display_threshold(fh, fc):
    fh = str(fh)
    fc = str(fc)
    threshold = ttk.Label(frame, text=fh + " FH " + fc + " FC", width=22)
    threshold.grid(row=1, column=1, columnspan=2)


def graph_switch():
    global fls_active
    if fls_active == 2:
        fls_active = 1
    else:
        fls_active = 2
    graph_background_create()


class AcBox(ttk.Frame):

    def __init__(self):
        super().__init__(master=root, padding=(5, 5))
        self.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky=NS)
        treev = ttk.Treeview(self, selectmode='browse', height=29)
        treev_columns = ("reg_num", "flight_h", "flight_c", "flight_h_daily", "flight_c_daily", "f_c_th_75x100", "f_c_th_56x75")
        column_counter = 0
        treev["columns"] = treev_columns
        treev["show"] = "headings"
        for column in treev_columns:
            display_order = partial(self.display_order, column)
            treev.column(column, width=90, anchor='center')
            treev.heading(column, text=heading_text[column_counter], command=display_order)
            column_counter += 1
        treev.grid(row=0, column=1)

        ac_box_scroll = ttk.Scrollbar(self, orient=VERTICAL, command=treev.yview)
        ac_box_scroll.grid(row=0, column=0, sticky=NS)
        treev['yscrollcommand'] = ac_box_scroll.set
        treev.bind('<<TreeviewSelect>>', self.treev_callback)
        self.treev = treev
        self.order_by = None

    def display_ac(self):
        for record in self.treev.get_children():
            self.treev.delete(record)
        db_conn = sqlite3.connect("AC data")
        db_cursor = db_conn.cursor()
        if self.order_by:
            db_cursor.execute(f"SELECT * FROM acData ORDER BY {self.order_by}")
        else:
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

    def display_order(self, column):
        if column != self.order_by:
            self.order_by = column
        else:
            self.order_by = self.order_by + " DESC"
        ac_box.display_ac()

    def treev_callback(self, _):
        treev_id = self.treev.selection()[0]
        reg_num, flight_h, flight_c, flight_h_daily, flight_c_daily, _, _ = self.treev.item(treev_id)["values"]
        input_box.insert_from_treev(reg_num, flight_h, flight_c, flight_h_daily, flight_c_daily)
        input_box.draw_graph()


graph_background_create()

input_box = InputBox()

ac_box = AcBox()
ac_box.display_ac()

graph_switch_btn = ttk.Button(frame, text="Change Graph", width=12, command=graph_switch)
graph_switch_btn.grid(row=1, column=4, columnspan=2)

root.mainloop()
