from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("FLS Threshold Calculator")

frame = LabelFrame(root, padx=5, pady=5)
frame.grid(padx=10, pady=10)

graph_1 = ImageTk.PhotoImage(Image.open("graph_1.bmp"))
graph_2 = ImageTk.PhotoImage(Image.open("graph_2.bmp"))

fls_active = 2
background_active = Label(frame)
background_active.grid(row=0, column=0, padx=20, pady=20)


def graph_background_create():
    global background_active
    background_active.grid_forget()
    if fls_active == 1:
        background_active = Label(frame, image=graph_1, bd=2, relief=SUNKEN)
    elif fls_active == 2:
        background_active = Label(frame, image=graph_2, bd=2, relief=SUNKEN)
    background_active.grid(row=0, column=0, padx=20, pady=20)
    return


def graph_switch():
    global fls_active
    if fls_active == 2:
        fls_active = 1
    else:
        fls_active = 2
    graph_background_create()
    return


graph_switch_button = Button(frame, text="Change Graph", command=graph_switch)
graph_switch_button.grid(row=1, column=0)
graph_background_create()


root.mainloop()
