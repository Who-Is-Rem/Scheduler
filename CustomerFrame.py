from tkinter import *
from tkinter import ttk
from People import *
from Service import *
from CustomTime import *

"""
Create a basic draggable frame
"""
class DnD(ttk.Frame):
    def __init__(self, parent, width=100, height=100):
        # Make the parent the root window so we can freely change between parents
        ttk.Frame.__init__(self, parent, width=width, height=height, style="Customer.TFrame")
        self.grid_propagate(False)
        self.bind_drag()

    def bind_drag(self):
        self.bind("<ButtonPress-1>", self.click)
        self.bind("<B1-Motion>", self.motion)

    def click(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

"""
Class that should support being gridded into a grid in the parent frame

The initial parent frame of thw dnd widget should ALWAYS be the root
This is to facilitate changing parent frame of the dragged widget

Once the widget is gridded, the size of the widget should change to match 
the size of the grid

For the scheculer the parent will ALWAYS be parent.parent else parent.winfo_toplevel()
"""
class DnDGrid(DnD):
    def __init__(self, tmpparent, parent):
        self.grid_coords = (-1, -1)

        super().__init__(tmpparent)
        self.parent = parent
        self.bind("<Map>", lambda e: self.configure(width=self.winfo_width(), height=self.winfo_height())
                  if self.grid_info() else None)

    def bind_drag(self):
        super().bind_drag()
        self.bind("<B1-ButtonRelease>", self.drop)

    def drop(self, event):
        widget = event.widget
        tmpx = widget.winfo_x()+(widget.winfo_width()//2)+(self.parent.parent.xview()[0]*self.parent.winfo_width())
        tmpy = widget.winfo_y()+(self.parent.parent.yview()[0]*self.parent.winfo_height())-35
        x, y = self.parent.grid_location(tmpx, tmpy)

        xmax, ymax = self.parent.grid_size()

        x = x+1 if x%self.parent.column_factor == 0 else x
        x = x-2 if x>=xmax == 0 else x

        y = y+1 if y%self.parent.row_factor == 0 else y
        y = y-2 if y>=ymax == 0 else y

        if x>=0 and y>=0 and x<xmax-1 and y<ymax-1:
            self.grid(in_=self.parent,row=y, column=x, sticky="nsew", padx=(0, 10))
            self.grid_coords = (x, y)
            self.event_generate("<<CustomerGrided>>")
        else:
            self.grid(in_=self.parent,row=self.grid_coords[1], column=self.grid_coords[0], sticky="nsew", padx=(0, 10))
"""
Should have a customer and alist of services as inputs
"""
class CustomerFrameBasic(DnDGrid):
    def __init__(self, parent, customer, services):
        super().__init__(parent)
        self.configure()
        assert isinstance(customer, Customer)
        abbrev = ""
        for serv in services: 
            assert isinstance(serv, Service)
            abbrev += f"{serv.getShort()} "

        self.price, self.time = services[0].addAll(services[1:]) if len(services)>1 else services[0].getPrice(), services[0].time_range
        customer_label = Label(self, text=f"{customer.getFirstName()}")
        services_label = Label(self, text=abbrev, wraplength=self.winfo_width(), anchor=NW)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        customer_label.grid(row=0, column=0, sticky="nsew")
        ttk.Separator(self, orient=HORIZONTAL).grid(row=1, column=0, sticky="nsew")
        services_label.grid(row=2, column=0, sticky="nsew")

    def drop(self, event):
        widget = event.widget
        x, y = self.parent.grid_location(widget.winfo_x()+widget.winfo_width()//2,widget.winfo_y()-35)
        xmax, ymax = self.parent.grid_size()
        if x>=0 and y>=0 and x<xmax-1 and y<ymax-1:
            self.grid(in_=self.parent,row=y, column=x, sticky="nsew")
        
        