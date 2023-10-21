from tkinter import *
from threading import Thread
from popUp import *
from scheduleSheet import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import *
import time, calendar

class Scheduler(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky="nsew")

        # ======== basic attributes ========
        self.datetime = datetime.today()
        self.datetimeVar = StringVar(value=self.datetime.date())

        # ======== Grid Configuration ========
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ======== Top Frame with Buttons ========
        self.topFrameHelper()
        self.calendar = CalendarFrame(self)
        self.calendar.bind("<Configure>", lambda e: self.calendar.place(x=(self.topFrame.winfo_width()//2)-(self.calendar.winfo_width()//2), y = self.topFrame.winfo_height()))

        # ======== Display Date ========
        self.dateLabel = Label(self, text=f"Date: {self.datetimeVar.get()}, {calendar.day_name[self.datetime.date().weekday()]}", bg="white", font=("Helvetica", 14))
        self.dateLabel.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # ======== Bottom Frame ========
        self.bottomFrameHelper()

        # PopUp Frame, for management
        self.popUp = Frame(self)

    def topFrameHelper(self):
        self.topFrame = Frame(self, bg="red")
        self.topFrame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # ======== Grid Configure ========
        self.topFrame.grid_rowconfigure([0,1], weight=1)
        self.topFrame.grid_columnconfigure([0,1,2],uniform="equal", weight=1)

        # ======== Creation of Buttons ========
        self.employeeButton = Button(self.topFrame, text="Employees", command= self.employeeButtonCommand)
        resetButton = Button(self.topFrame, text="Today", command= lambda: self.timeHelper(datetime.today()))
        serviceButton = Button(self.topFrame, text="Services", command= self.serviceButtonCommand)

        self.customerButton = Button(self.topFrame, text="Customers", bg="red", command=self.customerButtonCommand)

        dateFrame = Frame(self.topFrame, bg="red")
        dateFrame.grid_columnconfigure([0,1,2,3,4], weight=1)
        dateFrame.grid_rowconfigure(0, weight=1)
        prevBiWeeklyButton = Button(dateFrame, text="<<", command = lambda: self.timeHelper(self.datetime - timedelta(days=14)))
        prevButton = Button(dateFrame, text="<", command= lambda: self.timeHelper(self.datetime - timedelta(days=1)))
        dateButton = Button(dateFrame, text="Change Date", command= lambda: self.calendar.place(x=0, y=0))
        nextButton = Button(dateFrame, text=">", command= lambda: self.timeHelper(self.datetime + timedelta(days=1)))
        nextBiWeeklyButton = Button(dateFrame, text=">>", command= lambda: self.timeHelper(self.datetime + timedelta(days=14)))

        # ======== Grid Assign the Buttons ========
        self.employeeButton.grid(row=0, column=0, padx=4, pady=(4,2), sticky="nws")
        resetButton.grid(row=0, column=1, padx=4, pady=(4,2), sticky="ns")
        serviceButton.grid(row=0, column=2, padx=4, pady=4, sticky="nse")

        # For thread testing 
        tVar=StringVar()
        Button(self.topFrame, textvariable=tVar, command=lambda: tVar.set(active_count())).grid(row=0, column=0, padx=20)

        self.customerButton.grid(row=1, column=0, padx=4, pady=(2,4), sticky="nws")
        
        prevBiWeeklyButton.grid(row=0, column=0, sticky="ens", padx=2)
        prevButton.grid(row=0, column=1, sticky="ens", padx=2)
        dateButton.grid(row=0, column=2, sticky="nsew", padx=2)
        nextButton.grid(row=0, column=3, sticky="wns", padx=2)
        nextBiWeeklyButton.grid(row=0, column=4, sticky="nsw", padx=2)
        dateFrame.grid(row=1, column=1, sticky="ns", pady=(2,4))

        # ======= Bind the date time variable =======
        self.datetimeVar.trace("w", lambda *args: [self.scheduleSheet.setBool(False), self.scheduleSheet.updateGoogle.join(), self.scheduleSheet.updateGoogleDrive(),self.scheduleSheet.destroy(), self.canvas.delete(self.scheduleSheetID), Thread(target=self.scheduleThreadHelper).start()])

    def bottomFrameHelper(self):
        self.canvas = Canvas(self, highlightthickness=0)
        self.canvas.grid(row=2, column=1, sticky="nsew")
        
        Thread(target=self.scheduleThreadHelper).start()

    def scheduleThreadHelper(self):
        self.textID = self.canvas.create_text((self.winfo_width()//2, self.winfo_height()//2.5), text="Please Wait a Moment...", font=("Helvetica", 30))
        self.scheduleSheet = ScheduleSheet(self.canvas, str(self.datetime.date()))
        self.scheduleSheetID = self.canvas.create_window((0, 0), window=self.scheduleSheet, anchor="nw")
        self.canvas.delete(self.textID)
        
        # ======= Binding =======  
        self.scheduleSheet.bind("<Configure>",lambda e: [self.canvas.configure(scrollregion=self.canvas.bbox("all"))])
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.scheduleSheetID, width = self.canvas.winfo_width()))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta)), "units"))

        self.canvas.itemconfigure(self.scheduleSheetID, width = self.canvas.winfo_width())

    def timeHelper(self, datetime):
        self.datetime = datetime
        self.datetimeVar.set(datetime.date())
        self.dateLabel.configure(text=f"Date: {self.datetimeVar.get()}, {calendar.day_name[datetime.date().weekday()]}")

    # ======== Helper Function for Button Commands (Top Frame) ========
    def employeeButtonCommand(self):
        self.popUp.grid_forget()
        self.popUp = EmployeeToSchedule(self, "Employees")
        self.popUp.grid(row=1,rowspan=2, column=0, sticky="nsew")
        
        self.popUp.confirmButton.configure(command=self.addEmployeeToSchedule)
        
    def customerButtonCommand(self):
        self.popUp.grid_forget()
        self.popUp = CustomerToSchedule(self, "Customers")
        self.popUp.grid(row=1,rowspan=2, column=0, sticky="nsew")

        self.popUp.confirmButton.configure(command=self.addCustomerToSchedule)

    def serviceButtonCommand(self):
        self.popUp.grid_forget()
        self.popUp = ServiceToList(self, "Services")
        self.popUp.grid(row=1,rowspan=2, column=2, sticky="nsew")

    # ======= Bottom Frame =======
    def addEmployeeToSchedule(self):
        try: 
            emp = self.popUp.getEmployee()
            self.scheduleSheet.addEmployee(emp)
        except: 
            messagebox.showerror(title="Error", message=f"Failed to add {emp.getName()} to the Schedule")

    def addCustomerToSchedule(self):
        cust = self.popUp.getCustomer()
        if cust not in self.popUp.identifierList:
            self.popUp.addCustomerToList()
        self.scheduleSheet.addCustomerFrame(cust)
        self.popUp.grid_forget()

class CalendarFrame(Frame):
    def __init__(self, master):
        self.parent = master
        dateTup = (self.parent.datetimeVar.get()).split("-")
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

        chooseDate = Button(self, text="Select", command=self.setDate)
        chooseDate.grid(row=1, column=0, sticky="ws")

        cancel = Button(self, text="Cancel", command=lambda: self.place_forget())
        cancel.grid(row=1, column=0, sticky="es")
        
    def setDate(self):
        self.place_forget()
        self.parent.datetime = datetime.strptime(self.cal.get_date(), "%Y-%m-%d")
        self.parent.datetimeVar.set(self.parent.datetime)


