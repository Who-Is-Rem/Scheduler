from tkinter import *
from data import *
from tkinter import ttk, messagebox
import math

"""
Should be a frame holding all the information of the customer

Purely to make customer frame initialization and organiztion easier
"""
class CustomerFrame(Frame):
    def __init__(self, master, cust):
        Frame.__init__(self, master, bg="red", width=200, height=75, borderwidth=1, relief="solid")
        assert isinstance(cust, Customer)
        self.grid_propagate(False)

        self.colRow = (None, None)
        self.cust = cust

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        service_names = [s.getName() for s in cust.services]
        
        time_range = DataRange(0,0)
        price_range = DataRange(0,0)
        for s in cust.services:
            time_range = time_range.add(s.getTime())
            price_range = price_range.add(s.getPrice())
        self.min = time_range.getMin()
        self.max = time_range.getMax()
        self.extra = self.max - self.min

        self.rowspan = math.ceil(self.max/15)

        # ===== row 0 =====
        self.confirm_button = Label(self, text="✓", font=("Helvetica", 9))
        self.lock_button = Label(self, text="L", font=("Helvetica", 9))
        self.delete_button = Label(self, text="X", font=("Helvetica", 9))

        # ===== row 1 =====
        self.customer_information = Label(self, text=f"{cust.getName()} {cust.getLastNameShort()} #{cust.getNumber()}", anchor=NW, justify=LEFT)

        lockImage = PhotoImage(file="./lock.png").subsample(36,36)
        self.lockLabel = Label(self, image=lockImage, font=("Helvatica Bold", 26))
        self.lockLabel.img = lockImage

        # ===== row 2 =====
        ttk.Separator(self, orient=HORIZONTAL).grid(row=2, column=0, sticky="nsew")
        
        # ===== row 3 =====
        self.customer_services = Label(self, text=f"{', '.join(service_names)}", anchor=NW, justify=LEFT)
        self.price_label = Label(self, text=f"{price_range.getString()}")
        self.possibletime_frame = Frame(self, bg="red", width=10, height=self.extra//self.max)

        # ===== Grid Assignment =====
        self.grid_widgets()

        # Bindings
        if self.cust.locked:
            self.lockLabel.grid(row=0, column=0, sticky="ne")
            self.make_undraggable()
        else:
            self.make_draggable()
        self.customer_services.bind("<Configure>", lambda e: self.customer_services.configure(wraplength=self.customer_services.winfo_width()))
        self.lock_button.bind("<Button-1>", self.lockHelper)

        # self.bind("<Configure>", lambda e: [([self.configure(height=self.winfo_height()), self.configure(width=self.winfo_reqwidth())]) if self.winfo_width()==1 else self.winfo_width(), self.grid_widgets()])
        self.bind("<Configure>", lambda e: [self.configure(width=self.winfo_width(), height=self.winfo_height()) if self.colRow[0]!=None else None, self.grid_widgets(),self.update_idletasks()])
        self.bind("<Button-1>", self.on_click)

    def grid_widgets(self):
        self.confirm_button.grid(row=0, column=0, sticky="nsw", padx=3, pady=3)
        self.lock_button.grid(row=0, column=0, sticky="nsw", padx=21, pady=3)
        self.delete_button.grid(row=0, column=0, sticky="nse", padx=3, pady=3)
        self.customer_information.grid(row=1, column=0, sticky="nsew")
        self.customer_services.grid(row=3, column=0, sticky="nsew")
        self.price_label.grid(row=3, column=0, sticky="se", padx=(0, self.possibletime_frame.winfo_width()))
        self.possibletime_frame.grid(row=3, column=0, sticky="se") if self.possibletime_frame.winfo_height()>1 else None

    def lockHelper(self, e):
        self.cust.lockToggle()
        if self.cust.locked:
            self.make_undraggable()
            self.lockLabel.grid(row=1, column=0, sticky="ne")
        else:
            self.make_draggable()
            self.lockLabel.grid_forget()

    def on_click(self, e):
        self.lift()
        self.initX, self.initY = e.x, e.y

    def on_drag(self, e):
        x = self.winfo_x() - self.initX + e.x
        y = self.winfo_y() - self.initY + e.y
        self.place(x=x, y=y)

    def make_undraggable(self):
        self.bind("<B1-Motion>", lambda e: None)
    
    def make_draggable(self):
        self.bind("<B1-Motion>", self.on_drag)

