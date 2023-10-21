from tkinter import *
from data import *

# Making a frmae with grid configurations such that the first colums is (likely)
# smaller than that of the rest of the colums and the first and last rows having 
# 1 less weight such that the first and last rows have a weight of 1 while the 
# rest have weights of 2. In addtition 1 extra row compared to following columns

# Following colums should be able to have rows with weights of 1 
class scheduleSheet(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=master.winfo_width(), height=master.winfo_height())
        # Add a time frame to the left hand side of the canvas so that we can keep track of at what time employees have customers
        # should make it "unscrollable" in the x direction

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # =============== The Frame for Employee Names ===============
        self.enFrame = Frame(self, borderwidth=1, relief="solid")
        self.enFrame.grid_rowconfigure(0, weight=1)
        self.enFrame.grid(row=0, column=1,  sticky="new")

        # To keep track of employees
        self.employees = []

        # =============== The Frame for Time ===============
        self.timeFrame = Frame(self)
        self.timeFrame.grid(row=0, rowspan=2, column=0,sticky="nsw")
        self.timeFrame.grid_columnconfigure(0, weight=1)

        # Creation of time labels
        t = Time(8,0)
        for rowNum in range(50):
            self.timeFrame.grid_rowconfigure(rowNum, weight=1)
            l = Label(self.timeFrame, borderwidth=1, width=6, font=("Helvetica", 15))
            if rowNum == 0:
                # Spacer to account for Employee Name Frame
                l.configure(text="", height=1)
            else:
                l.configure(text=t.getTime(), height=2)
                t.next()
            l.grid(row=rowNum, column=0, sticky="nsew")

        # =============== The Frame for Customer Spread Sheet ===============
        self.spreadSheet = Frame(self, borderwidth=1, relief="solid")
        self.spreadSheet.grid_rowconfigure(0, weight=1)
        self.spreadSheet.grid(row=1, column=1, sticky="nsew")

    def addEmployeeColumn(self, emp):
        assert isinstance(emp, Employee)
        assert emp not in self.employees

        # =============== Add Employee Name ===============
        self.enFrame.grid_columnconfigure(len(self.employees)+1, weight=1)

        enLabel = Label(self.enFrame, text=emp.getFirstName(), font=("Helvetica Bold", 28))
        enLabel.grid(row=0, column=len(self.employees)+1, sticky="nsew")

        # =============== Add Customer Spreadsheet ===============
        # Note: Each "grid" should have a height of 2, use to name the labels
        self.spreadSheet.grid_columnconfigure(len(self.employees)+1, weight=1)

        # Creation of a frame to segregate each column of customers for employees
        self.customerColumn = Frame(self.spreadSheet)
        self.customerColumn.grid(row=0, column=len(self.employees)+1, sticky="nsew")
        self.customerColumn.grid_columnconfigure(0, weight=1)
        for rowNum in range(49):
            self.customerColumn.grid_rowconfigure(rowNum, weight=1)
            l = Label(self.customerColumn, borderwidth=1, height=2, relief="solid", font=("Helvetica", 15))
            if rowNum==48:
                l.configure(height=1, relief="flat")
            l.grid(row=rowNum, column=0, sticky="nsew")
        self.employees.append(emp)

# A string represtation of a 24hr clock
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