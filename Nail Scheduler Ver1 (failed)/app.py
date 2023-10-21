from tkinter import *
from mainFrame import *

# Creation of the main window with its frames
root = Tk()
root.title("Cara Nails Scheduler")
root.minsize(750,500)
root.maxsize(1440,900)
# root.geometry("750x500+345+170")
root.state("zoomed")

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.update_idletasks()

mFrame = mainFrame(root)

# Addition of employees testing
sheet = mFrame.getSheet()

root.mainloop()