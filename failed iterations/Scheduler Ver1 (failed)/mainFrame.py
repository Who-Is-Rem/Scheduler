from tkinter import *
from data import *
from datetime import date
import math
from centralFrame import *

class mainFrame(Frame):
    def __init__(self, master):
        # The top frame
        self.topFrame = Frame(master, bg = "red", width=master.winfo_width(), height=90, pady=3, padx=3)
        self.topFrame.grid(row=0, sticky="ew")

        # Configure the placement of the buttons and menu buttons
        self.topFrame.grid_columnconfigure(1, weight=1)
        self.topFrame.grid_columnconfigure(2, weight=0)
        self.topFrame.grid_rowconfigure(1, weight=1)
        
        row0buttonHelper(self, self.topFrame)
        row1ButtonHelper(self, self.topFrame)

        # The date label
        dateLabel = Label(master, text=f"Date: {date.today()}", font=('Helvatical',16))
        dateLabel.grid(row=1, column=0, sticky="we")

        # Central Frame
        self.centralFrame = centralFrame(master)

    # Creation of widgets within the popUp frmae causing it to "appear"
    # def employeeToList(self):
    #     self.leftPopUp.grid_forget()
    #     self.leftPopUp = EmployeeToList(self.cFrame, "Employees")

    # def employeeToSchedule(self):
    #     self.leftPopUp.grid_forget()
    #     self.leftPopUp = EmployeeToSchedule(self.cFrame, "Employees")

    # def customerToSchedule(self):
    #     self.leftPopUp.grid_forget()
    #     self.leftPopUp = CustomerToSchedule(self.cFrame, "Customers")

    # def customerToList(self):
    #     self.leftPopUp.grid_forget()
    #     self.leftPopUp = CustomerToList(self.cFrame, "Customers")

    # def serviceToList(self):
    #     self.rightPopUp.grid_forget()
    #     self.rightPopUp = ServiceToList(self.cFrame, "Services")

    # For scrolling anywhere on the canvas
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta)), "units")

    # Gets the inner frame where the schedule sheet is displayed
    def getSheet(self):
        return self.innerFrame

def row0buttonHelper(self, parentFrame):
        resetButton = Button(parentFrame, text = "Reset", bg="gray", padx = 1, pady = 1)
        employeeButton = Menubutton(parentFrame, text="Employees")
        serviceButton = Button(parentFrame, text="Service List",) # command=self.serviceToList

        employeeButton.menu = Menu(employeeButton, tearoff=0)
        employeeButton["menu"] = employeeButton.menu
        employeeButton.menu.add_command(label = "List of Employees",) # command=self.employeeToList
        employeeButton.menu.add_command(label = "Add Employee",) # command=self.employeeToSchedule

        employeeButton.grid(row=0, column=0, sticky="w", pady=2)
        resetButton.grid(row=0, column=1, pady=2)
        serviceButton.grid(row=0, column=2, sticky="e", pady=2)

def row1ButtonHelper(self, parentFrame):
        # Needs to be adjusted to add the pictures to the buttons, may end up using sprites 
        basePath = "/Users/al/Documents/csProjects/Nail Scheduler (py)/"
        nextPhoto = PhotoImage(file= basePath + "images/next.png").subsample(8,8)
        nextBiPhoto = PhotoImage(file=basePath + "images/nextBiweekly.png").subsample(8,8)
        prevPhoto = PhotoImage(file=basePath + "images/prev.png").subsample(8,8)
        prevBiPhoto = PhotoImage(file=basePath + "images/prevBiweekly.png").subsample(8,8)
        
        centralFrame = Frame(parentFrame, bg="red")
        leftFrame = Frame(centralFrame, bg="red")
        rightFrame = Frame(centralFrame, bg="red")

        customerButton = Menubutton(parentFrame, text="Customers")
        customerButton.menu = Menu(customerButton, tearoff=0)
        customerButton["menu"] = customerButton.menu
        customerButton.menu.add_command(label = "List of Customers", ) # command=self.customerToList
        customerButton.menu.add_command(label = "Add Customer", ) # command=self.customerToSchedule
        customerButton.grid(row=1, column=0, sticky = "w", pady=2)

        # left-central frame
        leftFrame.grid_columnconfigure(0, weight=1)
        leftFrame.grid_columnconfigure(1, weight=1)
        prevBiweeklyButton = Button(leftFrame, image = prevBiPhoto, bg="gray")
        previousButton = Button(leftFrame, image = prevPhoto, bg="gray")
        prevBiweeklyButton.grid(row=0, column=0, sticky="e")
        previousButton.grid(row=0, column=1, sticky="e", padx=4)
        prevBiweeklyButton.image = prevBiPhoto
        previousButton.image = prevPhoto

        # right-central frame
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_columnconfigure(1, weight=1)
        nextButton = Button(rightFrame, image = nextPhoto, bg="gray")
        nextBiweeklyButton = Button(rightFrame, image = nextBiPhoto, bg="gray")
        nextButton.grid(row=0, column=0, sticky="w", padx=4)
        nextBiweeklyButton.grid(row=0, column=1, sticky="w")
        nextBiweeklyButton.image = nextBiPhoto
        nextButton.image = nextPhoto

        # central frame
        centralFrame.grid_columnconfigure(2, weight=0)
        changeDate = Button(centralFrame, text = "Change Date", bg="gray", padx = 1, pady = 1)

        leftFrame.grid(row=0, column=0, padx=2, sticky="e")
        changeDate.grid(row=0, column=1, padx=2)
        rightFrame.grid(row=0, column=2, padx=2, sticky="w")

        centralFrame.grid(row=1, column=1, pady=2)