from tkinter import *
from scheduler import *

root = Tk()
root.minsize(750,500)
root.state("zoomed")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1) 

s = Scheduler(root)

root.mainloop()