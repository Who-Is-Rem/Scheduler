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
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def motion(self, event):
        x = self.winfo_x() - self._drag_start_x + event.x
        y = self.winfo_y() - self._drag_start_y + event.y
        self.place(x=x, y=y)

"""
Class that should support being gridded into a grid in the parent frame

The initial parent frame of thw dnd widget should ALWAYS be the root
This is to facilitate changing parent frame of the dragged widget

Once the widget is gridded, the size of the widget should change to match 
the size of the grid

For the scheculer the parent will ALWAYS be parent.parent else parent.winfo_toplevel()
"""
class DnDGrid(DnD):
    def __init__(self, parent, queue):
        self.grid_coords = (-1, -1)
        self.parent = parent
        self.queue = queue
        self.rowspan = 1

        super().__init__(parent.parent.parent)
        self.bind("<Map>", lambda e: [self.configure(width=self.winfo_width())]
                  if self.grid_info() else None)

    def bind_drag(self):
        super().bind_drag()
        self.bind("<B1-ButtonRelease>", self.drop)

    def drop(self, event):
        tmpx = self.winfo_x()+(self.winfo_width()//2)-self.parent.winfo_rootx()
        tmpy = self.winfo_y()+(self.parent.parent.yview()[0]*self.parent.winfo_height())-35
        x, y = self.parent.grid_location(tmpx, tmpy)

        xmax, ymax = self.parent.grid_size()

        x = x+1 if x%self.parent.column_factor == 0 else x
        x = x-2 if x>=xmax == 0 else x

        y = y+1 if y%self.parent.row_factor == 0 and y!=0 else y
        y = y-2 if y>=ymax == 0 else y

        if x>=0 and y>0 and x<xmax-1 and y<ymax-1:
            self.grid(in_=self.parent,row=y, column=x, rowspan=self.rowspan, sticky="nsew", padx=(0, 10))
            self.grid_coords = (x, y)
            self.event_generate("<<CustGrid>>")
        elif self.grid_coords == (-1, -1): 
            self.pack(in_=self.queue)
        else:
            self.grid(in_=self.parent,row=self.grid_coords[1], column=self.grid_coords[0], rowspan=self.rowspan, sticky="nsew", padx=(0, 10))
            self.event_generate("<<CustGrid>>")
        self.update_idletasks()

    def bindWidget(self, widget):
        widget.bind("<ButtonPress-1>", self.click)
        widget.bind("<B1-Motion>", self.motion)
        widget.bind("<B1-ButtonRelease>", self.drop)

"""
A Customer Frame with the relevant information to process their appointement efficiently
"""
class CustomerFrame(DnDGrid):
    def __init__(self, parent, queue, customer, services):
        assert isinstance(customer, Customer)
        assert len(services) != 0
        super().__init__(parent, queue)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        abbrev = f"{services[0].getShort():>5}: {services[0].getPrice()}"
        for serv in services[1:]: 
            assert isinstance(serv, Service)
            abbrev += f"\n{serv.getShort():>5}: {serv.getPrice()}"

        self.price, self.time = services[0].addAll(services[1:]) if len(services)>1 else (services[0].getPrice(), services[0].time_range)
        self.customer_label = Label(self, text=f"{customer.getFullName()}", 
                                    font = ("Helvetica", 16),
                                    anchor=NW)
        self.services_label = Label(self, text=abbrev, wraplength=self.winfo_reqwidth(), font=("PT mono", 14), anchor=NW)

        self.bindWidget(self.customer_label)
        self.bindWidget(self.services_label)

        self.rowspan = self.time.getMax().getTotalMinutes()//5 + self.time.getMax().getTotalMinutes()//15
        self.configure(height=(self.time.getMax().getTotalMinutes()*2)+(self.time.getMax().getTotalMinutes()//15))

        if self.rowspan > 1:
            self.customer_label.grid(row=0, column=0, sticky="nsew")
            self.services_label.grid(row=2, column=0, sticky="nsew")
            Label(self, text=f"Total: {self.price}", font=("PT mono", 14)).grid(row=2, column=0, sticky="sw")
        sep = ttk.Separator(self, orient=HORIZONTAL)
        sep.grid(row=1, column=0, sticky="nsew")
        self.bindWidget(sep)

    def drop(self, event):
        super().drop(event)
        self.services_label.configure(wraplength=self.winfo_width())