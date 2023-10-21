from tkinter import *
from data import *
from scheduleSheet import *
import pickle
from datetime import date

class topFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = "red", width=master.winfo_width(), height=90, pady=3, padx=3)
        # Configure the placement of the buttons and menu buttons
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        self.row0buttonHelper()
        self.row1ButtonHelper()

    def row0buttonHelper(self):
        self.resetButton = Button(self, text = "Reset", bg="gray", padx = 1, pady = 1)
        self.employeeButton = Menubutton(self, text="Employees")
        self.customerButton = Menubutton(self, text="Customers")

        self.employeeButton.menu = Menu(self.employeeButton, tearoff=0)
        self.customerButton.menu = Menu(self.customerButton, tearoff=0)

        self.employeeButton["menu"] = self.employeeButton.menu
        self.customerButton["menu"] = self.customerButton.menu

        self.employeeButton.menu.add_command(label = "add")
        self.employeeButton.menu.add_command(label = "list")
        self.customerButton.menu.add_command(label = "add")
        self.customerButton.menu.add_command(label = "list")

        self.employeeButton.grid(row=0, column=0, sticky="w", pady=2)
        self.customerButton.grid(row=0, column=2, sticky = "e", pady=2)
        self.resetButton.grid(row=0, column=1, pady=2)

    def row1ButtonHelper(self):
        # Needs to be adjusted to add the pictures to the buttons, may end up using sprites 
        basePath = "/Users/al/Documents/csProjects/Nail Scheduler (py)/"
        nextPhoto = PhotoImage(file= basePath + "images/next.png").subsample(6,6)
        nextBiPhoto = PhotoImage(file=basePath + "images/nextBiweekly.png").subsample(6,6)
        prevPhoto = PhotoImage(file=basePath + "images/prev.png").subsample(6,6)
        prevBiPhoto = PhotoImage(file=basePath + "images/prevBiweekly.png").subsample(6,6)
        
        leftFrame = Frame(self, bg="red")
        rightFrame = Frame(self, bg="red")

        # left frame
        leftFrame.grid_columnconfigure(0, weight=1)
        leftFrame.grid_columnconfigure(1, weight=1)
        self.prevBiweeklyButton = Button(leftFrame, image = prevBiPhoto, bg="gray")
        self.previousButton = Button(leftFrame, image = prevPhoto, bg="gray")
        self.prevBiweeklyButton.grid(row=0, column=0, sticky="e")
        self.previousButton.grid(row=0, column=1, sticky="e", padx=4)
        self.prevBiweeklyButton.image = prevBiPhoto
        self.previousButton.image = prevPhoto

        # right frame
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_columnconfigure(1, weight=1)
        self.nextButton = Button(rightFrame, image = nextPhoto, bg="gray")
        self.nextBiweeklyButton = Button(rightFrame, image = nextBiPhoto, bg="gray")
        self.nextButton.grid(row=0, column=0, sticky="w", padx=4)
        self.nextBiweeklyButton.grid(row=0, column=1, sticky="w")
        self.nextBiweeklyButton.image = nextBiPhoto
        self.nextButton.image = nextPhoto

        # middle
        self.changeDate = Button(self, text = "Change Date", bg="gray", padx = 1, pady = 1)

        leftFrame.grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.changeDate.grid(row=1, column=1, pady=2)
        rightFrame.grid(row=1, column=2, padx=2, pady=2, sticky="e")

class centralCanvas(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='purple', width=master.winfo_width(), height=master.winfo_height()-90)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        dateLabel = Label(self, text=f"Date: {date.today()}")
        dateLabel.grid(row=0, column=0, columnspan=3, sticky="we")

        vscrollBar = Scrollbar(self, orient=VERTICAL)
        hscrollBar = Scrollbar(self, orient=HORIZONTAL)
        self.canvas = Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand=vscrollBar.set, xscrollcommand=hscrollBar.set ,bg="yellow")
        vscrollBar.config(command=self.canvas.yview)
        hscrollBar.config(command=self.canvas.xview)

        self.canvas.grid(row=1, column=1, sticky="nsew")
        vscrollBar.grid(row=1, column=2, sticky="ns")
        hscrollBar.grid(row=2, column=1, sticky="ew")

        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        self.innerFrame = innerFrame = scheduleSheet(self.canvas)
        innerFrame.grid(row=0, column=1, sticky="nsew")
        innerFrameID = self.canvas.create_window(0,0,window=innerFrame, anchor="nw")

        innerFrame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(innerFrameID, width = self.canvas.winfo_width()))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.popUpFrame = Frame(self)
        self.popUpFrame.grid(row=0, column=1, sticky="nsew")

    def popUp(self, master):
        pass

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta)), "units")

    def getSheet(self):
        return self.innerFrame
