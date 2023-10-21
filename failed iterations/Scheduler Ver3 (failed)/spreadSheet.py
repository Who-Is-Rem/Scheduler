from tkinter import *
from data import *
from tkinter import messagebox
from customerFrame import *
import pickle
from graph import *
from googleDrive import *
from threading import *
import time

class CustomerSpreadSheet(Frame):
    def __init__(self, master, queue, date):
        self.parent = master
        self.queue = queue
        self.date = date
        self.customerGraph = Graph()

        Frame.__init__(self, master, name="spread sheet frame", bg="white")
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(list(range(50)), uniform="equal", weight=2)
        self.grid_rowconfigure(49, uniform="equal", weight=1)

        # Create a Label so as to show the scheduler is loading
        self.wait = Label(self, text="Please wait a moment", font=("Helvetica", 30), bg="white")
        self.wait.place(x=self.winfo_toplevel().winfo_width()//3, y=self.winfo_toplevel().winfo_height()//2-100)

        # To keep track of employees and frames
        self.employees = []
        self.employeesVar = StringVar()
        self.reset = []
        self.resetVar = StringVar()

        self.resetVar.trace("w", self.resetVarHelper)
        self.employeesVar.trace("w", self.employeeVarHelper)

        Thread(target=self.loadData).start()

    def loadData(self):
        # ===== Load google drive =====
        self.GD = ScheduleGoogleDrive()
        self.GD_file = self.GD.getPickleFile(str(self.date))
        self.GD_file.GetContentFile("./day.pickle")

        # ===== load from pickle =====
        with open("./day.pickle", "rb+") as path:
            empList = pickle.load(path)
            i = 0
            for emp in empList:
                self.addEmployeeColumn(emp)
                for cust in emp.customers:
                    self.addCustomerFrame(cust, i)
                i += 1
        self.wait.place_forget()

    def employeeVarHelper(self, *args):
        with open("./day.pickle", "rb+") as path:
            path.truncate(0)
            path.seek(0)
            pickle.dump(self.employees, path)
        
    def resetVarHelper(self, *args):
        self.reset.clear()
        self.reset.extend(self.employees)
        for w in self.winfo_children():
            w.grid_forget() 
        self.employees.clear()
        for e in self.reset:
            self.addEmployeeColumn(e) 
        self.grid_columnconfigure(len(self.employees), uniform="none", weight=0)
        self.employeesVar.set(self.employees)

    def addEmployeeColumn(self, emp):
        assert isinstance(emp, Employee)
        assert emp not in self.employees
        self.grid_columnconfigure(len(self.employees), uniform="equal",weight=1)

        for i in range(50):
            l = Label(self, text="", borderwidth=1, font=("Helvetica",16), bg="white")
            l.grid(row=i, column=len(self.employees), sticky="nsew")
            if i == 0:
                l.configure(text=f"{emp.getName()}", font=("Helvetica", 30))
                l.grid_columnconfigure(0, weight=1)
                b = Label(l, text="X", font=("Helvetica", 26))
                b.bind("<Button-1>", lambda e, emp=emp: messagebox.showerror(message="Employee has existing customers") 
                                                        if len(emp.getCustomers())!=0 
                                                        else [self.employees.remove(emp), self.resetVar.set(self.employees)])
                l.bind("<Enter>", lambda e, b=b: b.grid(column=0, row=0, sticky="nse"))
                l.bind("<Leave>", lambda e, b=b: b.grid_forget())
            elif i!=49:
                l.configure(relief="solid")
        self.employees.append(emp)
        self.employeesVar.set(self.employees)

    def addCustomerFrame(self, cust, col=-1):
        assert isinstance(cust, Customer)
        if len(cust.services) != 0:
            self.cF = CustomerFrame(self.parent, cust)

            self.cF.bind("<Button-1>", lambda e, cF = self.cF: ([self.employees[cF.colRow[0]].removeCustomer(cF.cust), 
                                                                 self.customerGraph.remove(cF.colRow[0], cF.colRow[1], cF.rowspan)]) 
                                                                 if cF.colRow!=(None, None) 
                                                                 else None, add="+")
            self.cF.bind("<B1-ButtonRelease>", lambda e, cF = self.cF: self.on_release(cF))
            self.cF.delete_button.bind("<Button-1>", lambda e, cf = self.cF: cf.destroy())

            if col!=-1:
                self.cF.grid(in_=self,column=col, row=cust.row, rowspan=self.cF.rowspan, sticky="nsew")
            else:
                self.cF.pack(in_=self.queue)
        else:
            messagebox.showerror(message="Please choose at least one service")
    
    def on_release(self, cF):
        x, y = self.grid_location(cF.winfo_x()-self.queue.winfo_width()+cF.winfo_width()//2,cF.winfo_y()+15)
        # within the spread sheet
        if x != -1 and y>0:
            try:
                self.customerGraph.occupy(x, y, cF.rowspan)
                cF.grid(in_=self, column=x, row=y, rowspan=cF.rowspan, sticky="nsew")
                cF.colRow = (x, y)
                cF.cust.row = y
                self.employees[x].addCustomer(cF.cust)
                self.employeesVar.set(self.employees)
            except GraphException:
                if cF.colRow == (None, None):
                    cF.pack(in_=self.queue)
                else:
                    cF.grid(in_=self, row=cF.colRow[1], column=cF.colRow[0], rowspan=cF.rowspan, sticky="nsew")
        else:
            if cF.colRow == (None, None):
                cF.pack(in_=self.queue)
            else:
                cF.grid(in_=self, row=cF.colRow[1], column=cF.colRow[0], rowspan=cF.rowspan, sticky="nsew")






