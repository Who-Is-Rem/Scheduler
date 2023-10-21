from tkinter import *
from tkinter import messagebox
import math, pickle
from data import *
from scheduleSheet import *

class listPopUp(Frame):
    def __init__(self, master, identifier):
        Frame.__init__(self, master, borderwidth=1, relief = "solid")
        self.grid(row=0, column=0,rowspan=2,sticky="nsew")
        self.identifier = identifier
        self.refreshPickle()
        
        self.grid_rowconfigure(6, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title = Label(self, font=("Helvetica", 20), borderwidth=1, relief="solid", width = 36)
        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Creation of confirmation button and close frame button
        self.bButtonFrame = Frame(self)
        self.bButtonFrame.grid_columnconfigure(0, weight =1)
        self.bButtonFrame.grid_columnconfigure(1, weight =1)
        self.confirmButton = Button(self.bButtonFrame, text = "Confirm")
        self.cancelButton = Button(self.bButtonFrame, text = "Cancel") 

        self.confirmButton.grid(row=0, column=0, padx=1, pady=1)
        self.cancelButton.grid(row=0, column=1, padx=1, pady=1)
        self.bButtonFrame.grid(row=6, column=1, sticky="ne", padx=2)
        
        self.searchFrame = Frame(self)
        self.searchFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.searchFrame.grid_columnconfigure(0, weight=1)

        self.searchBar = Entry(self.searchFrame, font=("Helvetica", 16))
        self.searchBar.grid(row=0, column=0, padx=(2,1), pady=2, sticky="nsew")

        self.tButtonFrame = Frame(self.searchFrame)
        self.tButtonFrame.grid_columnconfigure(0, weight =1)
        self.tButtonFrame.grid_columnconfigure(1, weight =1)
        self.removeButton = Button(self.tButtonFrame, text="Remove")
        self.removeButton.grid(row=0, column=0, sticky="nsew", padx=(0,1))
        self.editButton = Button(self.tButtonFrame, text="Edit")
        self.editButton.grid(row=0, column=1, sticky="nsew", padx=(1,0))
        self.tButtonFrame.grid(row=0, column=1, sticky="nse", padx=(1,2), pady=2) 

        # to remove an item from the list box
        def remove(e):
            typed = self.searchBar.get()
            try:
                index = self.listContents.index(typed)
                self.listContents.remove(typed)
                self.searchBar.delete(0, END)
                self.pickleDict.remove(self.identifierList[index], self.identifier)
                self.update(self.listContents)
            except: None

        # Put selected item in the lsitbox to the Entry
        def fillout(e):
            self.searchBar.delete(0,END)
            self.searchBar.insert(0, self.listBox.get(self.listBox.curselection()))

        def check(e):
            typed = self.searchBar.get()
            if typed == "":
                data = self.listContents
            else:
                data = []
                for item in self.listContents:
                    data.append(item) if typed.lower() in item.lower() else data
            self.update(data)

        self.listBox = Listbox(self, height=10, width = 10, font=("Helvetica", 16), selectmode=SINGLE)
        self.listBox.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=4, padx=4)

        self.update(self.listContents)
        self.listBox.bind("<<ListboxSelect>>", fillout)
        self.searchBar.bind("<KeyRelease>", check)
        self.removeButton.bind("<Button>", remove)
        self.cancelButton.bind("<Button>", lambda e: self.grid_forget())

    def refreshPickle(self):
    # To get the data from the pickle
        with open("/Users/al/Documents/csProjects/Nail Scheduler (py)/data.pickle", "rb") as path:
            self.pickleDict = pickle.load(path)
            self.identifierList = self.pickleDict.get(self.identifier)
            self.listContents = list(map(lambda i: i.getListContent(), self.identifierList))

    # Update the listbox
    def update(self, data):
        self.listBox.delete(0, END)
        for item in data:
            self.listBox.insert(END, item)

    # Helper function for creating frames for information of people
    def userInfo(self):
        # Configuration for the name entry area
        nameFrame = Frame(self)
        phoneFrame = Frame(self)
        nameFrame.grid(row=4, column=0, columnspan=2, sticky="new")
        phoneFrame.grid(row=5, column=0, columnspan=2, sticky="new", padx=2, pady=2)
        phoneFrame.grid_columnconfigure(0, weight=1)
        nameFrame.grid_columnconfigure(0, weight=1)

        fnFrame = Frame(nameFrame)
        lnFrame = Frame(nameFrame)

        # Widgets for the information of the person
        self.fnEntry = Entry(fnFrame, width=22)
        self.lnEntry = Entry(lnFrame, width=22)
        self.pnEntry = Entry(phoneFrame)
        fnLabel = Label(fnFrame, text="First Name")
        lnLabel = Label(lnFrame, text="Last Name")
        pnLabel = Label(phoneFrame, text="Phone Number")

        fnLabel.grid(row=0, column=0, sticky="nsw")
        self.fnEntry.grid(row=1, column=0,sticky="nsw")

        lnLabel.grid(row=0, column=0, sticky="nsw")
        self.lnEntry.grid(row=1, column=0,sticky="nse")

        pnLabel.grid(row=0, column=0, sticky="nsw")
        self.pnEntry.grid(row=1, column=0,sticky="nsewe")

        fnFrame.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        lnFrame.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)

    def deleteServiceEntries(self):
        self.nameEntry.delete(0, END)
        self.priceEntry.delete(0, END)
        self.timeEntry.delete(0, END)
        self.abbrevEntry.delete(0, END)

    def deletePeopleEntries(self):
        self.fnEntry.delete(0, END)
        self.lnEntry.delete(0, END)
        self.pnEntry.delete(0, END)

class EmployeeToList(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.title.config(text="List of Employees")
        self.confirmButton.configure(text="Add to List", command=self.addEmployeeToList)
        self.userInfo()

    def addEmployeeToList(self):        
        self.pickleDict.add(Customer(self.fnEntry.get(), self.lnEntry.get(), self.pnEntry.get()), self.identifier)
        self.deletePeopleEntries()
        self.refreshPickle()
        self.update(self.listContents)

class EmployeeToSchedule(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.removeButton.grid_forget()
        self.title.config(text="Add Employee to Schedule")
        self.confirmButton.config(text="Add to Schedule", command=self.addEmployeeToSchedule)

    def addEmployeeToSchedule(self):
        typed = self.searchBar.get()
        print(self.listContents)
        print(typed in self.listContents)
        print(self.listContents.index(typed))
        try: 
            index = self.listContents.index(typed)
            print(1)
            emp = self.identifierList[index]
            print(2)
            self.innerFrame
            print(3)
        except: None

class CustomerToSchedule(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.title.config(text="Add Customer to Schedule")
        self.confirmButton.config(text="Add to Schedule")
        self.selectedServices = []
        self.userInfo()

        servicesFrame = Frame(self)
        servicesFrame.grid_rowconfigure(0, weight=1)

        # Creation of the set of buttons to respond to what service a customer wants
        services = self.pickleDict.get("Services")
        for i in range(math.ceil(len(services)/5)):
            servicesFrame.grid_columnconfigure(i, weight=1)
            innerFrame = Frame(servicesFrame)
            innerFrame.grid_columnconfigure(0, weight=1)
            for ii in range(5):
                index = (i*5)+ii
                innerFrame.grid_rowconfigure(ii, weight=1)
                if (index<len(services)):
                    sb = Button(innerFrame, text=services[index].getListContent(), fg="red", font=("Helvetica", 16))
                    sb.bind("<Button>", lambda event, sb=sb, service = services[index]: [sb.configure(fg="green") if sb.cget("fg") == "red" else sb.configure(fg="red"), self.selectedServices.remove(service) if sb.cget("fg") == "red" and (service in self.selectedServices) else self.selectedServices.append(service)])
                    sb.grid(row=ii, column=0, pady=2, sticky="nsew")
            innerFrame.grid(row=0, column=i, padx=2 ,sticky="nsew")
        servicesFrame.grid(row=3, column=0, columnspan=2, sticky="nsew")


class CustomerToList(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.title.config(text="List of Customers")
        self.userInfo()

class ServiceToList(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.grid(row=0, column=3,rowspan=2,sticky="nsew")
        self.bButtonFrame.grid(row=6, column=0, sticky="w")
        self.title.config(text="List of Services")
        
        # Need to add functionality for name, price, and time, and abbreviated name
        leftFrame = Frame(self)
        leftFrame.grid(row=4, column=0, rowspan=2, sticky="nsew")
        leftFrame.grid_columnconfigure(0, weight=1)
        leftFrame.grid_rowconfigure(3, weight=0)
        rightFrame = Frame(self)
        rightFrame.grid(row=4, column=1, rowspan=2, sticky="nsew")
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_rowconfigure(3, weight=0)

        nameLabel = Label(leftFrame, text="Name")
        self.nameEntry = Entry(leftFrame)
        nameLabel.grid(row=0, column=0, sticky="nw", padx=2, pady=2)
        self.nameEntry.grid(row=1, column=0, sticky="nwe", padx=2, pady=2)

        priceLabel = Label(leftFrame, text="Price Range")
        self.priceEntry = Entry(leftFrame)
        priceLabel.grid(row=2, column=0, sticky="nw", padx=2, pady=2)
        self.priceEntry.grid(row=3, column=0, sticky="nwes", padx=2, pady=2)

        abbrevLabel = Label(rightFrame, text="Abbreviation")
        self.abbrevEntry = Entry(rightFrame)
        abbrevLabel.grid(row=0, column=0, sticky="nw", padx=2, pady=2)
        self.abbrevEntry.grid(row=1, column=0, sticky="nwe", padx=2, pady=2)

        timeLabel = Label(rightFrame, text="Time Range")
        self.timeEntry = Entry(rightFrame)
        timeLabel.grid(row=2, column=0, sticky="nw", padx=2, pady=2)
        self.timeEntry.grid(row=3, column=0, sticky="nwes", padx=2, pady=2)

        leftFrame.grid(row=4, column=0, rowspan=2, sticky="nsew", padx=2, pady=2)
        rightFrame.grid(row=4, column=1, rowspan=2, sticky="nsew", padx=2, pady=2)

        self.confirmButton.configure(command=self.serviceAdd)
    
    def serviceAdd(self):        
        self.pickleDict.add(Service(self.nameEntry.get(),PriceRange(self.priceEntry.get()),
                                TimeRange(self.timeEntry.get()),self.abbrevEntry.get()), self.identifier)
        self.deleteServiceEntries()
        self.refreshPickle()
        self.update(self.listContents)