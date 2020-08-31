from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("FLS Threshold Calculator")
root.geometry("800x600")

frame = LabelFrame(root, padx=5, pady=5)
frame.grid(padx=10, pady=10)

graph_75x100 = None
graph_56x75 = None
fls_active = 2
background_active = Label(frame)
background_active.grid(row=0, column=0, padx=20, pady=20)


def graph_background_create():
    global graph_75x100
    global graph_56x75
    global background_active
    graph_75x100 = ImageTk.PhotoImage(Image.open("graph_75x100.bmp"))
    graph_56x75 = ImageTk.PhotoImage(Image.open("graph_56x75.bmp"))
    background_active.grid_forget()
    if fls_active == 1:
        background_active = Label(frame, image=graph_75x100, bd=2, relief=SUNKEN)
    else:
        background_active = Label(frame, image=graph_56x75, bd=2, relief=SUNKEN)
    background_active.grid(row=0, column=0, padx=20, pady=20)


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
