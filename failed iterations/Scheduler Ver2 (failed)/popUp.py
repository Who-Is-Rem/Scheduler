from tkinter import *
from tkinter import messagebox, ttk
from data import *
import math
from threading import *


class listPopUp(Frame):
    def __init__(self, master, identifier):
        print("Super")
        Frame.__init__(self, master, borderwidth=1, relief = "solid")
        self.grid(row=0, column=0,rowspan=2,sticky="nsew")
        
        self.identifier = identifier

        # ========== Grid Config ==========
        self.grid_rowconfigure(6, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ========== refresh data dictionary ==========
        Thread(target=self.refreshPickle()).start()

        # ========== Zeroth Row ==========
        self.title = Label(self, font=("Helvetica", 20), borderwidth=1, relief="solid", width = 36)
        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # ========== First Row ==========
        searchFrame = Frame(self)
        searchFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        searchFrame.grid_columnconfigure(0, weight=1)

        # Search Bar
        self.searchBar = Entry(searchFrame, font=("Helvetica", 16))
        self.searchBar.grid(row=0, column=0, padx=(2,1), pady=2, sticky="nsew")
        self.searchBar.bind("<KeyRelease>", self.check)

        # Remove Item Buttons 
        self.tButtonFrame = Frame(searchFrame)
        self.tButtonFrame.grid_columnconfigure(0, weight =1)
        self.tButtonFrame.grid_columnconfigure(1, weight =1)
        self.tButtonFrame.grid_rowconfigure(0, weight=1)

        self.removeButton = Button(self.tButtonFrame, text="Remove")
        self.removeButton.grid(row=0, column=0, sticky="nsew", padx=2)

        self.tButtonFrame.grid(row=0, column=1, sticky="nse", pady=2) 

        # ========== Second Row ========== 
        self.listBox = Listbox(self, height=10, width = 10, font=("Helvetica", 16), selectmode=SINGLE, exportselection=False)
        self.listBox.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=4, padx=4)

        self.update(self.listContents)

        # ========== Sixth Row ==========
        # Creation of confirmation button and close frame button
        self.bButtonFrame = Frame(self)
        self.bButtonFrame.grid_columnconfigure(0, weight =1)
        self.bButtonFrame.grid_columnconfigure(1, weight =1)
        self.confirmButton = Button(self.bButtonFrame, text = "Confirm")
        self.cancelButton = Button(self.bButtonFrame, text = "Cancel") 

        self.confirmButton.grid(row=0, column=1, padx=2, sticky="e")
        self.cancelButton.grid(row=0, column=2, padx=2, sticky="e")
        self.bButtonFrame.grid(row=6, column=0, columnspan=2, sticky="nwe", pady=2)

        # Button Bindings
        self.cancelButton.bind("<Button>", lambda e: self.grid_forget())
        self.removeButton.bind("<Button>", self.remove)

        self.searchBar.focus_set()
        print("Super end")

    # ========== Create Bindings functions ==========
    # Binding for the remove Button
    def remove(self, e):
        typed = self.searchBar.get()
        try:
            index = self.listContents.index(typed)
            self.listContents.remove(typed)
            self.searchBar.delete(0, END)
            self.pickleDict.remove(self.identifierList[index], self.identifier)
            self.update(self.listContents)
        except: None

    def filloutPeople(self, e):
        selectedItem = self.listBox.get(self.listBox.curselection())
        self.searchBar.delete(0,END)
        self.searchBar.insert(0, selectedItem)
        cust = self.identifierList[self.listContents.index(selectedItem)]
        self.deletePeopleEntries()
        self.fnEntry.insert(0, cust.getFirstName())
        self.lnEntry.insert(0, cust.getLastName())
        self.pnEntry.insert(0, cust.getNumber())

    # Update the listbox by checking typed entry in the search bar
    def check(self, e):
        typed = self.searchBar.get()
        if typed == "":
            data = self.listContents
        else:
            data = []
            for item in self.listContents:
                data.append(item) if typed.lower() in item.lower() else data
        self.update(data)

    # ========== Helper Methods ==========
    # Refreshes the pickle dictionary to ensure constant flow of updated info
    def refreshPickle(self):
    # To get the data from the pickle
        with open("./data.pickle", "rb") as path:
            self.pickleDict = pickle.load(path)
            assert self.identifier in self.pickleDict.keys
            self.identifierList = self.pickleDict.get(self.identifier)
            self.listContents = list(map(lambda i: i.getListContent(), self.identifierList))

    # Update the listbox
    def update(self, data):
        self.listBox.delete(0, END)
        for item in data:
            self.listBox.insert(END, item)

    def userInfo(self):
        # ========== Fourth Row ==========
        # Frame for names
        nameFrame = Frame(self)
        nameFrame.grid(row=4, column=0, columnspan=2, sticky="new")
        nameFrame.grid_columnconfigure(0, weight=1)

        fnFrame = Frame(nameFrame)
        lnFrame = Frame(nameFrame)

        self.fnEntry = Entry(fnFrame, width=22)
        self.lnEntry = Entry(lnFrame, width=22)
        fnLabel = Label(fnFrame, text="First Name")
        lnLabel = Label(lnFrame, text="Last Name")

        fnLabel.grid(row=0, column=0, sticky="nsw")
        self.fnEntry.grid(row=1, column=0,sticky="nsw")
        lnLabel.grid(row=0, column=0, sticky="nsw")
        self.lnEntry.grid(row=1, column=0,sticky="nse")

        fnFrame.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        lnFrame.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)

        # ========== Fifth Row ==========
        # Frame for phone number
        phoneFrame = Frame(self)
        phoneFrame.grid(row=5, column=0, columnspan=2, sticky="new", padx=2, pady=2)
        phoneFrame.grid_columnconfigure(0, weight=1)

        self.pnEntry = Entry(phoneFrame)
        pnLabel = Label(phoneFrame, text="Phone Number")

        pnLabel.grid(row=0, column=0, sticky="nsw")
        self.pnEntry.grid(row=1, column=0,sticky="nsewe")

    def deleteServiceEntries(self):
        self.nameEntry.delete(0, END)
        self.priceEntry.delete(0, END)
        self.timeEntry.delete(0, END)
        self.abbrevEntry.delete(0, END)

    def deletePeopleEntries(self):
        self.fnEntry.delete(0, END)
        self.lnEntry.delete(0, END)
        self.pnEntry.delete(0, END)
    
    def getEmployee(self):
        return Employee(self.fnEntry.get(), self.lnEntry.get(), self.pnEntry.get())

    def addCustomerToList(self):
        self.pickleDict.add(self.getCustomer(), self.identifier)
        self.deletePeopleEntries()
        Thread(target=self.refreshPickle()).start()
        self.update(self.listContents)

    def addEmployeeToList(self):        
        self.pickleDict.add(self.getEmployee(), self.identifier)
        self.deletePeopleEntries()
        Thread(target = self.refreshPickle()).start()
        self.update(self.listContents)

class ServiceToList(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.grid(row=0, column=2, sticky="nsew")
        self.bButtonFrame.grid(row=6, column=0, sticky="w")
        self.title.config(text="List of Services")
        
        # ========== Fourth Row ==========
        # Row with name and abbreviation
        nameFrame = Frame(self)
        nameFrame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        nameFrame.grid_rowconfigure(1, weight=0)
        nameFrame.grid_columnconfigure(1, weight=0)

        nameLabel = Label(nameFrame, text="Name")
        self.nameEntry = Entry(nameFrame)
        abbrevLabel = Label(nameFrame, text="Abbreviation")
        self.abbrevEntry = Entry(nameFrame)

        nameLabel.grid(row=0, column=0, sticky="nsw", padx=2, pady=2)
        self.nameEntry.grid(row=1, column=0, sticky="nswe", padx=2, pady=2)
        abbrevLabel.grid(row=0, column=1, sticky="nsw", padx=2, pady=2)
        self.abbrevEntry.grid(row=1, column=1, sticky="nswe", padx=2, pady=2)

        # ========== Fifth Row ==========
        # Row with service data
        dataFrame = Frame(self)
        dataFrame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        dataFrame.grid_rowconfigure(1, weight=0)
        dataFrame.grid_columnconfigure(1, weight=0)

        priceLabel = Label(dataFrame, text="Price Range")
        self.priceEntry = Entry(dataFrame)
        timeLabel = Label(dataFrame, text="Time Range")
        self.timeEntry = Entry(dataFrame)

        priceLabel.grid(row=0, column=0, sticky="nsw", padx=2, pady=2)
        self.priceEntry.grid(row=1, column=0, sticky="nwes", padx=2, pady=2)
        timeLabel.grid(row=0, column=1, sticky="nsw", padx=2, pady=2)
        self.timeEntry.grid(row=1, column=1, sticky="nwes", padx=2, pady=2)

        # ========== Configure Confirm Button to Command ==========
        self.confirmButton.configure(command=self.serviceAdd)

        # ========== Binding ==========
        self.listBox.bind("<<ListboxSelect>>", self.filloutService)

    def filloutService(self, e):
        selectedItem = self.listBox.get(self.listBox.curselection())
        self.searchBar.delete(0,END)
        self.searchBar.insert(0, selectedItem)

        serv = self.identifierList[self.listContents.index(selectedItem)]
        self.deleteServiceEntries()
        self.nameEntry.insert(0, serv.getName())
        self.abbrevEntry.insert(0, serv.getShortName())
        self.priceEntry.insert(0, serv.getPrice().getString())
        self.timeEntry.insert(0, serv.getTime().getString())
    
    def serviceAdd(self):        
        self.pickleDict.add(Service(self.nameEntry.get(),PriceRange(self.priceEntry.get()),
                                TimeRange(self.timeEntry.get()),self.abbrevEntry.get()), self.identifier)
        self.deleteServiceEntries()
        Thread(target=self.refreshPickle()).start()
        self.update(self.listContents)

class CustomerToList(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.title.configure(text="List of All Customers")
        self.confirmButton.configure(text="Add to List", command=self.addCustomerToList)
        self.userInfo()

        # ========== Binding ==========
        self.listBox.bind("<<ListboxSelect>>", self.filloutPeople)

    def getCustomer(self):
        return Customer(self.fnEntry.get(), self.lnEntry.get(), self.pnEntry.get())

class CustomerToSchedule(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        self.title.config(text="Add Customer to Schedule")
        self.confirmButton.config(text="Add to Schedule")
        self.selectedServices = []
        self.userInfo()

        # Frame to put service buttons in
        servicesFrame = Frame(self)
        servicesFrame.grid_rowconfigure(0, weight=1)

        # Creation of the set of buttons to respond to what service a customer wants
        services = self.pickleDict.get("Services")
        for i in range(math.ceil(len(services)/7)):
            servicesFrame.grid_columnconfigure(i, uniform="equal" ,weight=1)
            innerFrame = Frame(servicesFrame)
            innerFrame.grid_columnconfigure(0,weight=1)
            for ii in range(7):
                index = (i*7)+ii
                innerFrame.grid_rowconfigure(ii, uniform="equal",weight=1)
                if (index<len(services)):
                    sb = Button(innerFrame, text=services[index].getListContent(), fg="red", font=("Helvetica", 16))
                    sb.bind("<Button>", lambda e, sb=sb, service = services[index]: [sb.configure(fg="green") if sb.cget("fg") == "red" else sb.configure(fg="red"), self.selectedServices.remove(service) if sb.cget("fg") == "red" and (service in self.selectedServices) else self.selectedServices.append(service)])
                    sb.grid(row=ii, column=0, pady=2, sticky="nsew")
            innerFrame.grid(row=0, column=i, padx=2 ,sticky="nsew")
        servicesFrame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # ========== Binding ==========
        self.listBox.bind("<<ListboxSelect>>", self.filloutPeople)

    def getCustomer(self):
        return Customer(self.fnEntry.get(), self.lnEntry.get(), self.pnEntry.get(), self.selectedServices)

class EmployeeToSchedule(listPopUp):
    def __init__(self, master, identifier):
        super().__init__(master, identifier)
        print("After Super")
        self.title.config(text="Add Employee to Schedule")
        self.confirmButton.config(text="Add to Schedule")

        self.listButton = Button(self.bButtonFrame,text="Add to List", command=self.addEmployeeToList)
        self.listButton.grid(row=0, column=0, sticky="w")
        self.userInfo()

        # ========== Binding ==========
        self.listBox.bind("<<ListboxSelect>>", self.filloutPeople)
        print("Pop up end")





class EmployeePopUp(Frame):
    def __init__(self, master):
        with open("./information/employees.pickle", "rb+") as path:
            self.employeeList = pickle.load(path)
            self.employeeListVar = StringVar()

        Frame.__init__(self, master, width=400)
        self.grid_columnconfigure(0, weight=1)

        # ===== row 0 =====
        self.title = Label(self, text="List of Employees", font=("Helvetica", 20), relief="solid", borderwidth=1)

        # ===== row 1 =====
        self.searchVar = StringVar()
        self.searchBar = Entry(self, textvariable=self.searchVar, font=("Helvetica", 18))
        self.remove_button = Button(self, text="Remove", command=self.removeEmployee)

        self.removeEntry_button = Label(self.searchBar, text="X", font=("Helvetica", 16), bg="white")
        self.removeEntry_button.pack(side=RIGHT)
        self.removeEntry_button.bind("<Button-1>", lambda e: self.searchBar.delete(0, END))

        # ===== row 2 =====
        self.listbox = Listbox(self, height=10, width = 10, font=("Helvetica", 18), selectmode=SINGLE, exportselection=False)

        # ===== row 3 =====
        nameFrame = Frame(self)
        nameFrame.grid_columnconfigure([0,1], uniform="equal", weight=1)
        nameFrame.grid_rowconfigure([0,1], uniform="equal", weight=1)

        # First Name
        firstName_label = Label(nameFrame, text="First Name")
        self.firstName_entry = Entry(nameFrame)

        firstName_label.grid(row=0, column=0, sticky="nsw")
        self.firstName_entry.grid(row=1, column=0, sticky="nsew")

        # Last Name
        lastName_label = Label(nameFrame, text="Last Name")
        self.lastName_entry = Entry(nameFrame)

        lastName_label.grid(row=0, column=1, sticky="nsw")
        self.lastName_entry.grid(row=1, column=1, sticky="nsew")

        # ===== row 4 =====
        numberFrame = Frame(self)
        numberFrame.grid_columnconfigure(0, weight=1)
        numberFrame.grid_rowconfigure([0,1], weight=1)

        number_label = Label(numberFrame, text="Phone Number")
        self.number_entry = Entry(numberFrame)

        number_label.grid(row=0, column=0, sticky="nsw")
        self.number_entry.grid(row=1, column=0, sticky="nsew")

        # ====== row 5 =====
        self.addList_button = Button(self,text="Add to List", command=lambda: [[self.employeeList.append(self.getEmployee()),
                                                                                self.employeeListVar.set(self.employeeList)] if self.getEmployee() not in self.employeeList
                                                                                else messagebox.showerror(message="Employee is already in the list"),
                                                                                self.searchBar.delete(0, END)
                                                                                ])
        self.confirm_button = Button(self, text="Add to Schedule")
        self.cancel_button = Button(self, text="Cancel", command=lambda: self.grid_forget())

        # ===== Separator for Asthetics =====
        ttk.Separator(self, orient=HORIZONTAL).grid(row=6, column=0, columnspan=3, sticky="nsew")

        # ===== grid assign =====
        self.title.grid(row=0, column=0, columnspan=2,sticky="nsew")
        self.searchBar.grid(row=1, column=0, sticky="nsew", pady=(4, 2))
        self.remove_button.grid(row=1, column=1, sticky="nsew", pady=(2, 2))
        self.listbox.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(2, 0), padx=4)
        nameFrame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        numberFrame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.addList_button.grid(row=5, column=0, sticky="nsw", pady=(0, 4))
        self.confirm_button.grid(row=5, column=0, sticky="nse", pady=(0, 4))
        self.cancel_button.grid(row=5, column=1, sticky="nsew", pady=(0, 4))

        # ===== bindings =====
        self.searchVar.trace("w", self.searchVarHelper)
        self.employeeListVar.trace("w", self.employeeListVarHelper)
        self.listbox.bind("<<ListboxSelect>>", self.listboxHelper)

        # ===== fill the list box during initialization =====
        self.searchVarHelper()

    def getEmployee(self):
        emp = Employee(self.firstName_entry.get(),
                        self.lastName_entry.get(),
                        self.number_entry.get())
        return emp

    def removeEmployee(self):
        emp = self.getEmployee()
        assert emp in self.employeeList
        self.employeeList.remove(emp)
        self.employeeListVar.set(self.employeeList)
        self.searchBar.delete(0, END)

    def listboxHelper(self, e):
        string = self.listbox.get(self.listbox.curselection())
        assert isinstance(string, str)
        fullname = string.strip().split(", ")[0]
        number = string.strip().split(", ")[1]
        self.searchBar.delete(0, END)
        self.firstName_entry.delete(0, END)
        self.lastName_entry.delete(0, END)
        self.number_entry.delete(0, END)
        self.searchBar.insert(0, fullname)
        self.firstName_entry.insert(0, fullname.split(" ")[0])
        self.lastName_entry.insert(0, fullname.split(" ")[1])
        self.number_entry.insert(0, number)

    def searchVarHelper(self, *args):
        self.listbox.delete(0, END)
        if self.searchVar.get() == "":
            for item in self.employeeList:
                self.listbox.insert(END, f"{item.getFullName()}, {item.getNumber()}")
        else:
            for item in self.employeeList:
                if (self.searchVar.get().lower() in item.getFullName().lower()) or self.searchVar.get() in item.getNumber():
                    self.listbox.insert(END, f"{item.getFullName()}, {item.getNumber()}")

    def employeeListVarHelper(self, *args):
        with open("./information/employees.pickle", "rb+") as path:
            path.truncate(0)
            path.seek(0)
            pickle.dump(self.employeeList, path)
        self.searchVarHelper() 

class ServicePopUp(Frame):
    def __init__(self, master):
        with open("./information/services.pickle", "rb+") as path:
            self.serviceList = pickle.load(path)
            self.serviceListVar = StringVar()

        Frame.__init__(self, master, width=400)
        self.grid_columnconfigure(1, weight=1)

        # ===== row 0 =====
        self.title = Label(self, text="List of Services", font=("Helvetica", 20), relief="solid", borderwidth=1)

        # ===== row 1 =====
        self.searchVar = StringVar()
        self.searchBar = Entry(self, textvariable=self.searchVar, font=("Helvetica", 18))
        self.remove_button = Button(self, text="Remove", command=self.removeService)

        self.removeEntry_button = Label(self.searchBar, text="X", font=("Helvetica", 16), bg="white")
        self.removeEntry_button.pack(side=RIGHT)
        self.removeEntry_button.bind("<Button-1>", lambda e: self.searchBar.delete(0, END))

        # ===== row 2 =====
        self.listbox = Listbox(self, height=10, width = 10, font=("Helvetica", 18), selectmode=SINGLE, exportselection=False)

        # ===== row 3 =====
        # Name of Service
        nameFrame = Frame(self)
        nameFrame.grid_columnconfigure([0,1], uniform="equal", weight=1)
        nameFrame.grid_rowconfigure([0,1], uniform="equal", weight=1)
        
        name_label = Label(nameFrame, text="Name of Service")
        self.name_entry = Entry(nameFrame)
        shortname_label = Label(nameFrame, text="Abbreviation")
        self.shortname_entry = Entry(nameFrame)

        name_label.grid(row=0, column=0, sticky="nsw")
        self.name_entry.grid(row=1, column=0, sticky="nsew")
        shortname_label.grid(row=0, column=1, sticky="nsw")
        self.shortname_entry.grid(row=1, column=1, sticky="nsew")

        # ===== row 4 =====
        # Price and time of service 
        dataFrame = Frame(self)
        dataFrame.grid_columnconfigure([0,1], uniform="equal", weight=1)
        dataFrame.grid_rowconfigure([0,1], uniform="equal", weight=1)

        price_label = Label(dataFrame, text="Price")
        self.price_entry = Entry(dataFrame)
        time_label = Label(dataFrame, text="Time")
        self.time_entry = Entry(dataFrame)

        price_label.grid(row=0, column=0, sticky="nsw")
        self.price_entry.grid(row=1, column=0, sticky="nsew")
        time_label.grid(row=0, column=1, sticky="nsw")
        self.time_entry.grid(row=1, column=1, sticky="nsew")

        # ====== row 5 =====
        self.addList_button = Button(self,text="Add to List", command=lambda: [self.serviceList.append(self.getService()),
                                                                                self.serviceListVar.set(self.serviceList)] if self.getService() not in self.serviceList
                                                                                else messagebox.showerror(message="Service is already in the list")
                                                                                )
        self.cancel_button = Button(self, text="Cancel", command=lambda: self.grid_forget())

        # ===== Separator for Asthetics =====
        ttk.Separator(self, orient=HORIZONTAL).grid(row=6, column=0, columnspan=3, sticky="nsew")

        # ===== grid assign =====
        self.title.grid(row=0, column=0, columnspan=2,sticky="nsew")
        self.searchBar.grid(row=1, column=0, sticky="nsew", pady=(4, 2))
        self.remove_button.grid(row=1, column=1, sticky="nsew", pady=(2, 2))
        self.listbox.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(2, 0), padx=4)
        nameFrame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        dataFrame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.addList_button.grid(row=5, column=0, sticky="nsw", pady=(0, 4))
        self.cancel_button.grid(row=5, column=1, sticky="nsew", pady=(0, 4))

        # ===== Binding =====
        self.searchVar.trace("w", self.searchVarHelper)
        self.serviceListVar.trace("w", self.serviceListVarHelper)
        self.listbox.bind("<<ListboxSelect>>", self.listboxHelper)

        # ===== fill the list box during initialization =====
        self.searchVarHelper()

    def getService(self):
        serv = Service(self.name_entry.get(), 
                       self.shortname_entry.get(), 
                       self.price_entry.get(), 
                       self.time_entry.get())
        return serv

    def removeService(self):
        serv = self.getService()
        assert serv in self.serviceList
        self.serviceList.remove(serv)
        self.serviceListVar.set(self.serviceList)
        self.searchBar.delete(0, END)

    def searchVarHelper(self, *args):
        self.listbox.delete(0, END)
        if self.searchVar.get() == "":
            for item in self.serviceList:
                self.listbox.insert(END, f"{item.getName()}, {item.getShort()}")
        else:
            for item in self.serviceList:
                if self.searchVar.get().lower() in item.getName().lower():
                    self.listbox.insert(END, f"{item.getName()}, {item.getShort()}")

    def listboxHelper(self, e):
        string = self.listbox.get(self.listbox.curselection())
        assert isinstance(string, str)
        name = string.strip().split(", ")[0]
        shortname = string.strip().split(", ")[1]
        self.searchBar.delete(0, END)
        self.name_entry.delete(0, END)
        self.shortname_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.time_entry.delete(0, END)

        self.searchBar.insert(0, name)
        
        for serv in self.serviceList:
            if serv.getName() == name and serv.getShort() == shortname:
                self.name_entry.insert(0, name)
                self.shortname_entry.insert(0, shortname)
                self.price_entry.insert(0, serv.getPrice().getString())
                self.time_entry.insert(0, serv.getTime().getString())
                break

    def serviceListVarHelper(self, *args):
        with open("./information/services.pickle", "rb+") as path:
            path.truncate(0)
            path.seek(0)
            pickle.dump(self.serviceList, path)
        self.searchVarHelper() 

class CustomerPopUp(Frame):
    def __init__(self, master):
        with open("./information/customers.pickle", "rb+") as path:
            self.customerList = pickle.load(path)
            self.customerListVar = StringVar()

        self.selected_services = []

        Frame.__init__(self, master, width=400)
        self.grid_columnconfigure(0, weight=1)

        # ===== row 0 =====
        self.title = Label(self, text="List of Customers", font=("Helvetica", 20), relief="solid", borderwidth=1)

        # ===== row 1 =====
        self.searchVar = StringVar()
        self.searchBar = Entry(self, textvariable=self.searchVar, font=("Helvetica", 18))
        self.remove_button = Button(self, text="Remove", command=self.removeCustomer)

        self.removeEntry_button = Label(self.searchBar, text="X", font=("Helvetica", 16), bg="white")
        self.removeEntry_button.pack(side=RIGHT)
        self.removeEntry_button.bind("<Button-1>", lambda e: self.searchBar.delete(0, END))

        # ===== row 2 =====
        self.listbox = Listbox(self, height=10, width = 10, font=("Helvetica", 18), selectmode=SINGLE, exportselection=False)

        # ===== row 3 =====
        self.serviceFrame = Frame(self)
        with open("./information/services.pickle", "rb") as path:
            slist = pickle.load(path)

            self.serviceFrame.grid_columnconfigure(list(range(math.ceil(len(slist)/6))), uniform="equal" ,weight=1) 
            if len(slist) >=6: self.serviceFrame.grid_rowconfigure(list(range(6)), uniform="equal",weight=1)
            else: self.serviceFrame.grid_rowconfigure(list(range(len(slist))), uniform="equal", weight=1)

            for i in range(len(slist)):
                l = Label(self.serviceFrame, text=f"{slist[i].getName()}", relief="solid", fg="red", borderwidth=1, font=("Helvetica", 18))
                l.bind("<Button-1>", lambda e, l=l, serv=slist[i]: [l.configure(fg="green") if l.cget("fg")=="red" else l.configure(fg="red"), 
                                                                    self.selected_services.append(serv) if l.cget("fg")=="green" else self.selected_services.remove(serv)])
                l.grid(column=i//6, row=i%6, sticky="nsew", padx=2, pady=2)

        # ===== row 4 =====
        nameFrame = Frame(self)
        nameFrame.grid_columnconfigure([0,1], uniform="equal", weight=1)
        nameFrame.grid_rowconfigure([0,1], uniform="equal", weight=1)

        # First Name
        firstName_label = Label(nameFrame, text="First Name")
        self.firstName_entry = Entry(nameFrame)

        firstName_label.grid(row=0, column=0, sticky="nsw")
        self.firstName_entry.grid(row=1, column=0, sticky="nsew")

        # Last Name
        lastName_label = Label(nameFrame, text="Last Name")
        self.lastName_entry = Entry(nameFrame)

        lastName_label.grid(row=0, column=1, sticky="nsw")
        self.lastName_entry.grid(row=1, column=1, sticky="nsew")

        # ===== row 5 =====
        numberFrame = Frame(self)
        numberFrame.grid_columnconfigure(0, weight=1)
        numberFrame.grid_rowconfigure([0,1], weight=1)

        number_label = Label(numberFrame, text="Phone Number")
        self.number_entry = Entry(numberFrame)

        number_label.grid(row=0, column=0, sticky="nsw")
        self.number_entry.grid(row=1, column=0, sticky="nsew")

        # ====== row 6 =====
        self.addList_button = Button(self,text="Add to List", command=lambda: [[self.customerList.append(self.getCustomer()),
                                                                                self.customerListVar.set(self.customerList)] if self.getCustomer() not in self.customerList
                                                                                else messagebox.showerror(message="Customer is already in the list"),
                                                                                self.searchBar.delete(0, END)])
        self.confirm_button = Button(self, text="Add to Schedule")
        self.cancel_button = Button(self, text="Cancel", command=lambda: self.grid_forget())

        # ===== Separator for Asthetics =====
        ttk.Separator(self, orient=HORIZONTAL).grid(row=7, column=0, columnspan=3, sticky="nsew")

        # ===== grid assign =====
        self.title.grid(row=0, column=0, columnspan=2,sticky="nsew")
        self.searchBar.grid(row=1, column=0, sticky="nsew", pady=(4, 2))
        self.remove_button.grid(row=1, column=1, sticky="nsew", pady=(2, 2))
        self.listbox.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(2, 0), padx=4)
        self.serviceFrame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(4,0))
        nameFrame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        numberFrame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.addList_button.grid(row=6, column=0, sticky="nsw", pady=(0, 4))
        self.confirm_button.grid(row=6, column=0, sticky="nse", pady=(0, 4))
        self.cancel_button.grid(row=6, column=1, sticky="nsew", pady=(0, 4))

        # ===== bindings =====
        self.searchVar.trace("w", self.searchVarHelper)
        self.customerListVar.trace("w", self.customerListVarHelper)
        self.listbox.bind("<<ListboxSelect>>", self.listboxHelper)

        # ===== fill the list box during initialization =====
        self.searchVarHelper()

    def getCustomer(self):
        cust = Customer(self.firstName_entry.get(), 
                        self.lastName_entry.get(), 
                        self.number_entry.get(),
                        self.selected_services)
        return cust

    def removeCustomer(self):
        cust = self.getCustomer()
        assert cust in self.customerList
        self.customerList.remove(cust)
        self.customerListVar.set(self.customerList)
        self.searchBar.delete(0, END)

    def listboxHelper(self, e):
        string = self.listbox.get(self.listbox.curselection())
        assert isinstance(string, str)
        fullname = string.strip().split(", ")[0]
        number = string.strip().split(", ")[1]
        self.searchBar.delete(0, END)
        self.firstName_entry.delete(0, END)
        self.lastName_entry.delete(0, END)
        self.number_entry.delete(0, END)
        self.searchBar.insert(0, fullname)
        self.firstName_entry.insert(0, fullname.split(" ")[0])
        self.lastName_entry.insert(0, fullname.split(" ")[1])
        self.number_entry.insert(0, number)

        for w in self.serviceFrame.winfo_children():
            w.configure(fg="red")
        self.selected_services.clear()

    def searchVarHelper(self, *args):
        self.listbox.delete(0, END)
        if self.searchVar.get() == "":
            for item in self.customerList:
                self.listbox.insert(END, f"{item.getFullName()}, {item.getNumber()}")
        else:
            for item in self.customerList:
                if (self.searchVar.get().lower() in item.getFullName().lower()) or self.searchVar.get() in item.getNumber():
                    self.listbox.insert(END, f"{item.getFullName()}, {item.getNumber()}")

    def customerListVarHelper(self, *args):
        with open("./information/customers.pickle", "rb+") as path:
            path.truncate(0)
            path.seek(0)
            pickle.dump(self.customerList, path)
        self.searchVarHelper() 


