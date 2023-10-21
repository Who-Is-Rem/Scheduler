from tkinter import *
from tkcalendar import Calendar
import calendar as cal
import datetime
from datetime import *
from spreadSheet import *
from data import *
from tkinter import ttk
from popUp import *
from customerFrame import *
from datetime import *
from threading import *

"""
Where the creation of all the widgets occur
"""

class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # To force the grids for pop ups to shrink
        Frame(self, height=1, width=1, bg="Purple").grid(row=0,column=0, rowspan=1000, sticky="s")
        Frame(self, height=1, width=1).grid(row=0,column=5, rowspan=1000, sticky="s")

        # ===== Stuff related to dates =====
        self.date = date.today()
        self.dateVar = StringVar(value=self.date)
        self.calendar_frame = CalendarFrame(self)
        self.calendar_frame.bind("<Configure>", lambda e: self.calendar_frame.place(x=(self.winfo_width()//2)-(self.calendar_frame.winfo_width()//2), y = self.r12BG.winfo_height()))

        # ===== Background creation for rows 0 & 1 =====
        self.r12BG = Frame(self, bg="red")
        self.r12BG.grid(row=0, column=0, rowspan=2, columnspan=5, sticky="nsew")
        self.r12BG.lower()

        # ===== row 0 =====
        self.employee_button = Button(self, text="Employees", command= self.employeeButtonCommand)
        self.reset_buttom = Button(self, text="Today", command=lambda: None)
        self.services_button = Button(self, text="Services", command= self.serviceButtonCommand)

        self.employee_button.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=4, pady=(4,2))
        self.reset_buttom.grid(row=0, column=2, sticky="ns", padx=4, pady=(4,2))
        self.services_button.grid(row=0, column=3, columnspan=2, sticky="nse", padx=4, pady=4)

        # ===== row 1 =====
        self.customer_button = Button(self, text="Customers", bg="red", command=self.customerButtonCommand)

        dateFrame = Frame(self, bg="red")
        dateFrame.grid_rowconfigure(0, weight=1)
        dateFrame.grid_columnconfigure([0,1,2,3,4], weight=0)
        self.left_button = Button(dateFrame, text="<", command=lambda: self.dateChangeHelper(self.date-timedelta(days=1)), bg="red")
        self.left2_button = Button(dateFrame, text="<<", command=lambda: self.dateChangeHelper(self.date-timedelta(days=14)), bg="red")
        self.calendar_button = Button(dateFrame, text="Calendar", bg="red", command=lambda: self.calendar_frame.place(x=1, y=1) if self.calendar_frame.place_info() == {} else self.calendar_frame.place_forget())
        self.right2_button = Button(dateFrame, text=">>", command=lambda: self.dateChangeHelper(self.date+timedelta(days=14)), bg="red")
        self.right_button = Button(dateFrame, text=">", command=lambda: self.dateChangeHelper(self.date+timedelta(days=1)), bg="red")

        self.left_button.grid(row=0, column=0, sticky="nsew", padx=2)
        self.left2_button.grid(row=0, column=1, sticky="nsew", padx=2)
        self.calendar_button.grid(row=0, column=2, sticky="nsew", padx=2)
        self.right2_button.grid(row=0, column=3, sticky="nsew", padx=2)
        self.right_button.grid(row=0, column=4, sticky="nsew", padx=2)

        self.customer_button.grid(row=1, column=0, columnspan=2, sticky="nsw", padx=4, pady=(2,4))
        dateFrame.grid(row=1, column=2, sticky="ns", padx=4, pady=(2,4))
        

        # ===== row 2 =====
        self.dateVar = StringVar()
        self.date_label = Label(self, text=f"Date: {date.today()}, {cal.day_name[date.today().weekday()]}", font=("helvetica", 16))
        self.date_label.grid(row=2, column=0, columnspan=5, sticky="nsew")

        # ===== row 3 =====
        ttk.Separator(self, orient=HORIZONTAL).grid(row=3, column=0, columnspan=5, sticky="nsew", padx=0, pady=0, ipadx=0, ipady=0)

        # ===== row 4 =====
        self.popUp = Frame(self)
        self.canvas = Canvas(self, highlightthickness=0)

        self.canvas.grid(row=4, column=1, columnspan=3, sticky="nsew")

        # ===== Within the Canvas =====
        self.canvas_frame = Frame(self.canvas, relief="solid")
        self.canvas_frameID = self.canvas.create_window((0,0), anchor=NW, window=self.canvas_frame)

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(3, weight=1)

        self.update_idletasks()
        self.canvas.itemconfigure(self.canvas_frameID, width = self.canvas.winfo_width())

        # frame widgets in the canvas frame
        self.customerList_frame = Frame(self.canvas_frame, name="customer list frame")
        self.time_frame = Frame(self.canvas_frame, name="time frame", bg="white")
        self.spreadSheet_frame = CustomerSpreadSheet(self.canvas_frame, self.customerList_frame, self.date)

        # to force the customer list frame to shrink
        Frame(self.customerList_frame, height=1, width=1).pack(side=BOTTOM, fill=X, expand=TRUE)

        # Helper Methods
        self.timeFrame_helper()

        # Grid the frame widgets
        ttk.Separator(self.canvas_frame, orient=VERTICAL).grid(row=0, column=0, sticky="ns")
        self.customerList_frame.grid(row=0, column=1, sticky="nsew")
        self.time_frame.grid(row=0, column=2, sticky="nsew")
        self.spreadSheet_frame.grid(row=0, column=3, sticky="nsew")
        ttk.Separator(self.canvas_frame, orient=VERTICAL).grid(row=0, column=4, sticky="ns")

        # ===== Bindings =====
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.canvas_frameID, width = self.canvas.winfo_width()))
        self.spreadSheet_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1*(e.delta), "units") if e.state==0 else self.canvas.xview_scroll(-1*(e.delta), "units"))
        self.dateVar.trace("w", self.dateVarHelper)

    def timeFrame_helper(self):
        self.time_frame.grid_columnconfigure(0, weight=1)
        self.time_frame.grid_rowconfigure(list(range(50)), uniform="equal",weight=2)
        self.time_frame.grid_rowconfigure(0, uniform="equal",weight=1)

        t = TIME(8, 0)
        for i in range(49):
            l = Label(self.time_frame, text=f"{t.sh}:{t.sm}", font=("Helvetica", 20), bg="white")
            l.grid(row=i+1, column=0, sticky="nsew")
            t.next()

    def dateChangeHelper(self, time):
        self.date = time
        self.dateVar.set(time)
        self.date_label.configure(text=f"Date: {self.date}, {cal.day_name[self.date.weekday()]}", font=("helvetica", 16))

    def dateVarHelper(self, *args):
        self.spreadSheet_frame.GD_file.SetContentFile("./day.pickle")
        self.spreadSheet_frame.GD_file.Upload()
        self.spreadSheet_frame.grid_forget()
        self.spreadSheet_frame.destroy()
        self.spreadSheet_frame = CustomerSpreadSheet(self.canvas_frame, self.customerList_frame, self.date)
        self.spreadSheet_frame.grid(row=0, column=3, sticky="nsew")

    # ===== Pop Up Frames from Employee, Customer, and Service Buttons =====
    def employeeButtonCommand(self):
        self.popUp.grid_forget()
        self.popUp = EmployeePopUp(self)
        self.popUp.grid(row=3, rowspan=2, column=0, sticky="nsew")

        self.popUp.confirm_button.configure(command=lambda: [[self.popUp.employeeList.append(self.popUp.getEmployee()), self.popUp.employeeListVar.set(self.popUp.getEmployee())] if self.popUp.getEmployee() not in self.popUp.employeeList else None,
                                                             self.spreadSheet_frame.addEmployeeColumn(self.popUp.getEmployee()),
                                                             self.popUp.searchBar.delete(0, END)
                                                             ])

    def serviceButtonCommand(self):
        self.popUp.grid_forget()
        self.popUp = ServicePopUp(self)
        self.popUp.grid(row=3, rowspan=2, column=4, sticky="nsew")

    def customerButtonCommand(self):
        self.popUp.grid_forget()
        self.popUp = CustomerPopUp(self)
        self.popUp.grid(row=3, rowspan=2, column=0, sticky="nsew")

        self.popUp.confirm_button.configure(command= lambda: self.spreadSheet_frame.addCustomerFrame(self.popUp.getCustomer()) if len(self.spreadSheet_frame.employees)!=0 else messagebox.showerror(message="Please have at least one employee on the Scheduler"))

class TIME():
    def __init__(self, h, m):
        assert h >= 0 and m >= 0
        self.sh = "0"+str(h) if len(str(h)) == 1 else str(h)
        self.sm = "0"+str(m) if len(str(m)) == 1 else str(m)
        self.h = h
        self.m = m

    def next(self):
        self.m += 15
        if self.m >= 60:
            self.h += 1
            self.m = 0
        self.sh = "0"+str(self.h) if len(str(self.h)) == 1 else str(self.h)
        self.sm = "0"+str(self.m) if len(str(self.m)) == 1 else str(self.m)

class CalendarFrame(Frame):
    def __init__(self, master):
        self.parent = master
        dateTup = (self.parent.dateVar.get()).split("-")
        Frame.__init__(self, master.winfo_toplevel(), width = 400, height=300, relief="solid", borderwidth=2)
        self.grid_propagate(False)
        style = ttk.Style(self)
        style.theme_use('clam')  
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.cal = Calendar(self, selectmode = 'day', year = int(dateTup[0]), month = int(dateTup[1]),day = int(dateTup[2]),date_pattern = "yyyy-mm-dd",
                       background = "grey",
                       firstweekday = "sunday", showweeknumbers=False,
                       font = ("Helvetica, 16")
                       )
        self.cal.grid(row=0, column=0, sticky="nsew")

        self.chooseDate = Button(self, text="Select", command=self.setDate)
        self.chooseDate.grid(row=1, column=0, sticky="ws")

        cancel = Button(self, text="Cancel", command=lambda: self.place_forget())
        cancel.grid(row=1, column=0, sticky="es")
        
    def setDate(self):
        self.place_forget()
        self.parent.date = (datetime.strptime(self.cal.get_date(), "%Y-%m-%d")).date()
        self.parent.dateVar.set(self.parent.date)

        







 