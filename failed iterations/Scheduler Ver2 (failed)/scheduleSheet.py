from tkinter import *
from googleDrive import *
from threading import *
from data import *
from customerFrame import *
import time, datetime

class ScheduleSheet(Frame):
    def __init__(self, master, date):
        # ======= Basic Attributes ======= 
        self.date = date
        self.employees = []

        self.overlapDict = {}
        self.resetList = []

        Frame.__init__(self, master, relief="solid", borderwidth=1)
        self.grid_rowconfigure(list(range(49)), uniform="equal", weight=1)

        # ======= Creation of Time Frame =======
        timeFrame = Frame(self, bg="white")
        timeFrame.grid(row=0, rowspan=50, column=1,sticky="nsw")
        timeFrame.grid_columnconfigure(0, weight=1)

        # Creation of time labels
        t = Time(8,0)
        timeFrame.grid_rowconfigure(list(range(1,50)), uniform="equal" ,weight=2)
        timeFrame.grid_rowconfigure(0, uniform="equal",weight=1)
        for rowNum in range(50):
            l = Label(timeFrame, borderwidth=1, width=6, font=("Helvetica", 15), bg="white")
            if rowNum == 0:
                # Spacer to account for Employee Name Frame
                l.configure(text="", height=1)
            else:
                l.configure(text=t.getTime())
                t.next()
            l.grid(row=rowNum, column=0, sticky="nsew")

        # ======= Initialization of Schedule if there is an existing one ======= 
        self.GD = ScheduleGoogleDrive()
        self.picklefile = self.GD.getPickleFile(self.date)
        self.picklefile.GetContentFile("day.pickle")

        with open("./day.pickle", "rb+") as path:
            empList = pickle.load(path)
            index = 2
            for emp in empList:
                self.addEmployee(emp)
                for cust in emp.customers:
                    self.addCustomerFrame(cust, index)
                index += 1

        self.updateBool = True

        # ======= Auto upload to google drive periodically =======
        self.updateGoogle = Thread(target=self.updateGoogleDriveHelper)
        self.updateGoogle.start()

        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", lambda: [self.setBool(False), self.updateGoogle.join(), self.picklefile.SetContentFile("day.pickle"), self.picklefile.Upload(), self.winfo_toplevel().destroy()])

    def reset(self):
        self.grid_columnconfigure(len(self.employees)+2, weight=0, uniform="min")
        for widget in self.resetList:
            widget.grid_forget()
        self.resetList.clear()
        i = 2
        temp = self.employees.copy()
        self.employees.clear()
        for emp in temp:
            self.addEmployee(emp)
            for cust in emp.customers:
                self.addCustomerFrame(cust, i)
            i += 1

    def setBool(self, boolean):
        self.updateBool = boolean

    def updateGoogleDriveHelper(self):
        while self.updateBool:
            start = time.time()
            time.sleep(0.5)
            self.updateGoogleDrive()
            end = time.time()
            print(end-start)
    
    def updateGoogleDrive(self):
        with open("./day.pickle", "rb+") as path:
            path.seek(0)
            path.truncate()
            pickle.dump(self.employees, path)
        self.picklefile.SetContentFile("day.pickle")
        self.picklefile.Upload()

    def addEmployee(self, emp):
        assert emp not in self.employees
        assert isinstance(emp, Employee)
        self.grid_columnconfigure(len(self.employees)+2,uniform="equal",weight=1)

        # Creation of label for employee name
        nameLabel = Label(self, text=emp.getFirstName(), font=("Helvetica Bold", 28), bg="white")
        nameLabel.grid(row=0, column=len(self.employees)+2, sticky="nsew")
        nameLabel.grid_columnconfigure(0, weight=1)
        nameLabel.grid_propagate(False)
        self.resetList.append(nameLabel)
        
        deleteButton = Label(nameLabel, text="X")
        deleteButton.bind("<Button-1>", lambda e, emp=emp: ([self.employees.remove(emp), self.reset()]) if len(emp.customers)==0 else messagebox.showerror(message="Employee column has customers in it!"))

        # Creation of Grids for the employee column
        for rowNum in range(49):
            l = Label(self, borderwidth=1, relief="solid", font=("Helvetica", 15), bg="white")
            if rowNum==48:
                l.configure(relief="flat")
            l.grid(row=rowNum+1, column=len(self.employees)+2, sticky="nsew")
            self.resetList.append(l)
        self.employees.append(emp)
        
        # ======= Binding =======
        nameLabel.bind("<Enter>", lambda e: deleteButton.grid(row=0, column=0, sticky="ne"))
        nameLabel.bind("<Leave>", lambda e: deleteButton.grid_forget())

    def addCustomerFrame(self, cust, col=0):
        if len(self.employees) == 0: messagebox.showerror(message="Please have at least one employee on the schedule!")
        cF = CustomerFrame(self, cust, col)

        if col>1: self.resetList.append(cF)

    # To check if there are any overlaps between customer frames
    def overlap(self, col, row, rowspan, cust):
        if col not in self.overlapDict.keys():
            self.overlapDict[col] = set(range(row, row+rowspan))
        else:
            for i in range(row, row+rowspan):
                if i in self.overlapDict[col]:
                    return True
            self.overlapDict[col] = self.overlapDict[col].union(set(range(row, row+rowspan)))
        cust.row = row
        self.employees[col-2].customers.append(cust)
        return False
    
    def deleteRows(self, col, row, rowspan):
        if col in self.overlapDict.keys():
            l = list(map(lambda i: self.overlapDict[col].remove(i), list(range(row, row+rowspan))))
            if self.overlapDict[col] == set():
                self.overlapDict.__delitem__(col)

class Time():
    def __init__(self, ihour, iminute):
        assert 0 <= ihour <= 23
        assert 0 <= iminute < 59
        assert iminute % 15 == 0
        self.hour = ihour
        self.min = iminute

    # Returns the string representation of the current time
    def getTime(self):
        smin = str(self.min)
        smin = "0" + smin if len(smin) == 1 else smin
        return str(self.hour) + ":" + smin
    
    def getNext(self):
        min = 0; hour = 0
        if (self.min+15 >= 60):
            hour = self.hour + 1
            if (self.hour >= 24):
                hour = 0
        else: 
            min = self.min + 15
        return Time(hour, min)
    
    # Forwards the time by 15 minutes
    # e.g. 8:00 gives 8:15
    def next(self):
        if (self.min+15 >= 60):
            self.min = 0
            self.hour += 1
            if (self.hour >= 24):
                self.hour = 0
        else: 
            self.min+=15


