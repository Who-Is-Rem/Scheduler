from tkinter import *
import pickle, math
from data import *
from tkinter import ttk, messagebox

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
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=2, rowspan=6, sticky="nsew")
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
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=0, rowspan=6, sticky="nsew")
        ttk.Separator(self, orient=HORIZONTAL).grid(row=6, column=0, columnspan=3, sticky="nsew")

        # ===== grid assign =====
        self.title.grid(row=0, column=1, columnspan=2,sticky="nsew")
        self.searchBar.grid(row=1, column=1, sticky="nsew", pady=(4, 2))
        self.remove_button.grid(row=1, column=2, sticky="nsew", pady=(2, 2))
        self.listbox.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=(2, 0), padx=4)
        nameFrame.grid(row=3, column=1, columnspan=2, sticky="nsew")
        dataFrame.grid(row=4, column=1, columnspan=2, sticky="nsew")
        self.addList_button.grid(row=5, column=1, sticky="nsw", pady=(0, 4))
        self.cancel_button.grid(row=5, column=2, sticky="nsew", pady=(0, 4))

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

            if len(slist) > 0:
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
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=2, rowspan=6, sticky="nsew")
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


