from tkinter import *
from data import *
from tkinter import ttk
import time
from threading import *

# Creation of a draggable customer Frame
class CustomerFrame(Frame):
    def __init__(self, master, cust, col):
        assert isinstance(cust, Customer)
        if len(cust.desiredServices) == 0: messagebox.showerror(message="Please select at least one service for the Customer!")

        # ======= Basic Attributes =======
        self.parent = master
        self.cust = cust

        self.minRows = cust.expectedTime().getMin()//15
        self.maxRows = cust.expectedTime().getMax()//15
        self.extraRows = self.maxRows-self.minRows
        servicesList = ", ".join(list(s.getName() for s in cust.desiredServices))

        Frame.__init__(self, master, width=200, bg=self.cust.bg, borderwidth=1, relief="solid")
        self.grid_propagate(False)
        self.grid(row=cust.row, column=col, rowspan=self.maxRows, sticky="nsew")
        self.colRow = (col,cust.row)

        # ======= Grid Configure =======
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ======= Creation of inner Widgets =======
        lockImage = PhotoImage(file="./lock.png").subsample(18,18)
        self.custInfo = Label(self, text=f"{cust.getName()}\n#: {cust.getNumber()}", font=("Helvatica Bold", 14), anchor = W,justify=LEFT, borderwidth=0)
        self.separator = ttk.Separator(self, orient=HORIZONTAL)
        self.custServices = Label(self, text=servicesList, font=("Helvatica", 14), justify=LEFT, anchor = NW, borderwidth=0, wraplength=200)
        self.possibleTimeFrame = Frame(self, bg=self.cust.bg)
        self.lockLabel = Label(self, image=lockImage, font=("Helvatica Bold", 26))
        self.lockLabel.img = lockImage

        # Buttons 
        self.removeButton = Label(self, text="X", font=("Helvetica", 8))
        self.completedButton = Label(self, text="✓", font=("Helvetica", 8))
        self.lockButton = Label(self, text="L", font=("Helvetica", 8))

        # ======= Grid Assignment =======
        self.gridWidgets()

        # ======= Binding =======
        # Binding for DnD
        if self.cust.locked:
            self.lockLabel.grid(row=0, column=0, sticky="ne", pady=(20,0))
        else:
            self.bind("<Button-1>", self.pressed)
            self.bind("<B1-Motion>", lambda e: Thread(target=self.dragMotion(e)).start())
            self.bind("<B1-ButtonRelease>", self.release)
        self.bind("<Configure>", lambda e: [self.configure(width=self.winfo_width(), height=self.winfo_height()),self.possibleTimeFrame.configure(width=15, height=int(self.winfo_height()*(self.extraRows/self.maxRows))) if self.minRows != self.maxRows else None,self.gridWidgets()])
        self.custServices.bind("<Configure>", lambda e: self.custServices.configure(wraplength=self.custServices.winfo_width()))

        # Buttons
        self.lockButton.bind("<Button-1>", self.lockHelper)
        self.removeButton.bind("<Button-1>", lambda e: [self.parent.deleteRows(self.colRow[0], self.colRow[1], self.maxRows), self.parent.employees[self.colRow[0]-2].customers.remove(self.cust), self.grid_forget()])
        self.completedButton.bind("<Button-1>", lambda e, self=self: [self.configure(bg="green"),self.possibleTimeFrame.configure(bg="green"), self.cust.setBg("green")])

    def lockHelper(self, e):
        self.parent.employees[self.colRow[0]-2].customers.remove(self.cust)
        self.cust.lockToggle()
        if self.cust.locked:
            self.lockLabel.grid(row=0, column=0, sticky="ne", pady=(20,0))
            self.bind("<Button-1>", lambda e: None)
            self.bind("<B1-Motion>", lambda e: None)
            self.bind("<B1-ButtonRelease>", lambda e: None)  
        else:
            self.lockLabel.grid_forget()
            self.bind("<Button-1>", self.pressed)
            self.bind("<B1-Motion>", lambda e: Thread(target=self.dragMotion(e)).start())
            self.bind("<B1-ButtonRelease>", self.release)
        self.parent.employees[self.colRow[0]-2].customers.append(self.cust)

    # To get the initial posiiton of the widget for smoother motion of the widget
    def pressed(self, e):
        self.initX, self.initY = e.x, e.y
        self.parent.deleteRows(self.colRow[0],self.colRow[1], self.maxRows)
        if self.colRow[0] > 1: 
            self.parent.employees[self.colRow[0]-2].customers.remove(self.cust)

    # The widget should follow the mouse pointer
    def dragMotion(self, e):
        self.lift()
        x = self.winfo_x() - self.initX + e.x
        y = self.winfo_y() - self.initY + e.y
        self.place(x=x, y=y)

    # Grid assignment once released
    def release(self, e):
        x,y = self.parent.grid_location(self.winfo_x()+(self.winfo_width()//2), self.winfo_y()+(self.winfo_height()//(self.maxRows*2)))
        if x>1 and y>0:
            if self.parent.overlap(x, y, self.maxRows, self.cust):
                self.grid(row=self.colRow[1],column=self.colRow[0], sticky="nsew", rowspan=self.maxRows)
            else: 
                self.grid(row=y, column=x, sticky="nsew", rowspan=self.maxRows)
                self.colRow = (x, y)
            if self not in self.parent.resetList: self.parent.resetList.append(self)
        else: 
            self.grid(row=self.colRow[1], column=self.colRow[0], rowspan=self.maxRows, sticky="nsew")
            if self.colRow[0] > 1 and self.colRow[1]>0:
                self.parent.employees[self.colRow[0]-2].customers.append(self.cust)
    
    def gridWidgets(self):
        self.custInfo.grid(row=0, column=0, sticky="nsew", ipadx=0, ipady=1, padx=0, pady=(20,0))
        self.separator.grid(row=1, column=0, sticky="nsew")
        self.custServices.grid(row=2, column=0, sticky="nsew", ipadx=0, ipady=0, padx=0, pady=0)
        self.possibleTimeFrame.grid(row=0, column=0, rowspan=3, sticky="se")

        self.completedButton.grid(row=0, column=0, sticky="nw", padx=2, pady=2)
        self.lockButton.grid(row=0, column=0, sticky="nw", padx=(18,0), pady=2)
        self.removeButton.grid(row=0, column=0, sticky="ne", padx=2, pady=2)









