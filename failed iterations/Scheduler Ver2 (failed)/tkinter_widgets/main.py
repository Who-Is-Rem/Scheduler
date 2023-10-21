from tkinter import *
from spreadSheet import *

root = Tk()
root.configure(bg="red")
root.state("zoomed")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

ss = SpreadSheet(root, 5, 5)
ss.addFrame(0,0)
ss.addFrame(4,4)

dnd1 = ss.addDnD()
dnd1.grid(row=0, column=1, sticky="nsew")
dnd1.configure(bg="red")

b1 = dnd1.addButton()
b1.grid(row=0, column=0, sticky="nw")
b1.configure(text="Hello", command=lambda: print("Hello"))

root.mainloop()