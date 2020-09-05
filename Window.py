from tkinter import *
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = Tk()
root.title("FLS Threshold Calculator")
root.geometry("800x800")

frame = LabelFrame(root, padx=5, pady=5)
frame.grid(padx=10, pady=10)

fls_active = 2
graph_active = Label(frame)
graph_active.grid(row=0, column=0, padx=20, pady=20)


def graph_background_create():
    global graph_active
    if fls_active == 1:
        graph_75x100 = Figure(figsize=(6, 5), dpi=100)
        graph_75x100.add_subplot(111).plot([0, 45, 100, 100], [75, 75, 30, 0], "-k")
        graph_active = FigureCanvasTkAgg(graph_75x100, master=frame)
        graph_active.draw()
    else:
        graph_56x75 = Figure(figsize=(6, 5), dpi=100)
        graph_56x75.add_subplot(111).plot([0, 33, 75, 75], [56, 56, 22, 0], "-k")

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


data_win_op_btn = Button(root, text="Data table", command=open_data_win)
data_win_op_btn.grid(row=1, column=0)

graph_switch_btn = Button(frame, text="Change Graph", command=graph_switch)
graph_switch_btn.grid(row=1, column=0)

graph_background_create()


root.mainloop()
