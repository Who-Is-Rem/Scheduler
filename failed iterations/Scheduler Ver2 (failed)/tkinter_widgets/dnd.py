from tkinter import *
from threading import *

# Creation of a drag and dropable frame
# Frame should automatically fit into a grid once dropped

# Is NOT initially gridded into the parent frame

class DnD(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid_propagate(False)
        self.parent = master
        self.rowspan, self.columnspan = 1,1

        # ======= Binding for DnD =======
        self.bind("<Button-1>", self.pressed)
        self.bind("<B1-Motion>", self.dragMotion) 
        self.bind("<B1-ButtonRelease>", self.release)
        
        # Binding for size changes
        self.bind("<Configure>", lambda e: self.configure(width=self.winfo_width(), height=self.winfo_height()))

    # To get the initial posiiton of the widget for smoother motion of the widget
    def pressed(self, e):
        self.initX, self.initY = self.winfo_pointerxy()

    # The widget should follow the mouse pointer
    def dragMotion(self, e):
        mx, my = self.winfo_pointerxy()
        dx, dy = mx-self.initX, my-self.initY
        self.initX, self.initY = self.winfo_pointerxy()
        self.place(x=self.winfo_x()+dx,y=self.winfo_y()+dy)

    # Grid assignment once released
    def release(self, e):
        mx, my = self.winfo_pointerxy()
        x,y = self.parent.grid_location(mx, my)
        self.grid(row=y, column=x, sticky="nsew", columnspan=self.columnspan, rowspan=self.rowspan)

    # To set row and column span attributes
    def setRowSpan(self, rs):
        self.rowspan = rs

    def setColSpan(self, cs):
        self.columnspan = cs

    # Helper function for adding widgets in the DnD Frame
    def addFrame(self):
        f = Frame(self)
        f.bind("<Button-1>", self.pressed)
        f.bind("<B1-Motion>", self.dragMotion) 
        f.bind("<B1-ButtonRelease>", self.release)
        return f
    
    def addLabel(self):
        l = Label(self)
        l.bind("<Button-1>", self.pressed)
        l.bind("<B1-Motion>", self.dragMotion) 
        l.bind("<B1-ButtonRelease>", self.release)
        return l
    
    def addButton(self):
        b = Button(self)
        b.bind("<Button-1>", self.pressed)
        b.bind("<B1-Motion>", self.dragMotion) 
        b.bind("<B1-ButtonRelease>", self.release)
        return b

