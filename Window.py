from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = Tk()
root.title("FLS Threshold Calculator")
root.geometry("800x800")

frame = LabelFrame(root, padx=5, pady=5)
frame.grid(row=0, column=0, padx=10, pady=10)

fls_active = 2
graph_active = Label(frame)
graph_active.grid(row=0, column=0, padx=20, pady=20)

input_label = Label()


def input_box():
    reg_n_len = StringVar()
    fl_h_len = StringVar()
    fl_c_len = StringVar()
    fl_h_d_len = StringVar()
    fl_c_d_len = StringVar()

    def entry_limit(sv):
        c = sv.get()[0:9]
        sv.set(c)

    def val_int(input_str, char_name):
        if char_name == "1":
            if not input_str.isdigit():
                return False
        return True

    def data_check(button):
        data_status = ""
        global input_label
        input_label.grid_forget()
        if flight_h.get() == "" or \
                flight_h_daily.get() == "" or \
                flight_c_daily.get() == "":
            data_status = "Please,\n fill all fields"
            check = False
        else:
            if reg_num.get() == "" and button == "save":
                data_status = "Please,\n fill all fields"
                check = False
            else:
                if button == "save":
                    data_status = "Saved"
                check = True
        input_label = Label(entry_frame, text=data_status, fg="red")
        input_label.grid(row=0, column=5)
        return check

    def save_info():
        if data_check("save"):
            input_info = [reg_num.get(),
                          flight_h.get(),
                          flight_c.get(),
                          flight_h_daily.get(),
                          flight_c_daily.get()]

    def draw_graph():
        if data_check("draw"):
            input_info = [reg_num.get(),
                          flight_h.get(),
                          flight_c.get(),
                          flight_h_daily.get(),
                          flight_c_daily.get()]

    entry_frame = LabelFrame(root, padx=5, pady=5)
    entry_frame.grid(row=1, column=0, padx=10, pady=10, sticky=W)

    Label(entry_frame, text="Registration\nNumber").grid(row=0, column=0)
    reg_num = Entry(entry_frame, width=10, textvariable=reg_n_len)
    reg_n_len.trace("w", lambda *args: entry_limit(reg_n_len))
    reg_num.grid(row=1, column=0)

    Label(entry_frame, text="Flight Hours\n ").grid(row=0, column=1)
    flight_h = Entry(entry_frame, validate="key", width=10, textvariable=fl_h_len)
    fl_h_len.trace("w", lambda *args: entry_limit(fl_h_len))
    flight_h.configure(validatecommand=(flight_h.register(val_int), '%P', '%d'))
    flight_h.grid(row=1, column=1)

    Label(entry_frame, text="Flight Cycles\n ").grid(row=0, column=2)
    flight_c = Entry(entry_frame, validate="key", width=10, textvariable=fl_c_len)
    fl_c_len.trace("w", lambda *args: entry_limit(fl_c_len))
    flight_c.configure(validatecommand=(flight_c.register(val_int), '%P', '%d'))
    flight_c.grid(row=1, column=2)

    Label(entry_frame, text="Flight Hours\nDaily").grid(row=0, column=3)
    flight_h_daily = Entry(entry_frame, validate="key", width=10, textvariable=fl_h_d_len)
    fl_h_d_len.trace("w", lambda *args: entry_limit(fl_h_d_len))
    flight_h_daily.configure(validatecommand=(flight_h_daily.register(val_int), '%P', '%d'))
    flight_h_daily.grid(row=1, column=3)

    Label(entry_frame, text="Flight Cycles\nDaily").grid(row=0, column=4)
    flight_c_daily = Entry(entry_frame, validate="key", width=10, textvariable=fl_c_d_len)
    fl_c_d_len.trace("w", lambda *args: entry_limit(fl_c_d_len))
    flight_c_daily.configure(validatecommand=(flight_c_daily.register(val_int), '%P', '%d'))
    flight_c_daily.grid(row=1, column=4)

    save_btn = Button(entry_frame, text="Save", command=save_info, width=12)
    save_btn.grid(row=1, column=5)

    draw_btn = Button(entry_frame, text="Draw", command=draw_graph, width=12)
    draw_btn.grid(row=1, column=6)


def graph_background_create():
    global graph_active
    if fls_active == 1:
        graph_75x100 = Figure(figsize=(6, 5), dpi=100)
        plot = graph_75x100.add_subplot(111)
        plot.plot([0, 45, 100, 100], [75, 75, 30, 0], "-k")
        plot.plot([0, 50], [0, 30], "-r")

        graph_active = FigureCanvasTkAgg(graph_75x100, master=frame)
        graph_active.draw()
    else:
        graph_56x75 = Figure(figsize=(6, 5), dpi=100)
        plot = graph_56x75.add_subplot(111)
        plot.plot([0, 33, 75, 75], [56, 56, 22, 0], "-k")
        plot.plot([0, 50], [0, 30], "-r")

        graph_active = FigureCanvasTkAgg(graph_56x75, master=frame)
        graph_active.draw()
    graph_active.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)


def graph_switch():
    global fls_active
    if fls_active == 2:
        fls_active = 1
    else:
        fls_active = 2
    graph_background_create()


def open_data_win():
    data_win = Toplevel()
    data_win.title("Data")
    data_win.geometry("600x600")
    vert_slider = Scale(data_win)
    vert_slider.grid(row=0, column=1)


graph_background_create()

input_box()

graph_switch_btn = Button(frame, text="Change Graph", width=12, command=graph_switch)
graph_switch_btn.grid(row=1, column=0)

data_win_op_btn = Button(root, text="Data table", width=12, command=open_data_win)
data_win_op_btn.grid(row=3, column=0, padx=10, pady=10, sticky=W)

root.mainloop()
