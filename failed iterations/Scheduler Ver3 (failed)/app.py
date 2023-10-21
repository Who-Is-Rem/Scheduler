from tkinter import *
from mainFrame import *
from threading import *
import time

root = Tk()

root.state("zoomed")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

mf = MainFrame(root)

root.update_idletasks()

root.mainloop()