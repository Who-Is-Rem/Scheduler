from Service import *
import pickle

"""
Class that represents a person
"""
class Person():
    def __init__(self, first_name, last_name, phone_num):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(phone_num, str)
        self.fname = first_name
        self.lname = last_name
        self.full = f"{first_name} {last_name}"
        self.phone = phone_num

    def __eq__(self, other):
        assert isinstance(other, Person)
        return self.full==other.full

    def getFirstName(self):
        return self.fname
    
    def getLastName(self):
        return self.lname
    
    def getFullName(self):
        return self.full
    
    def getPhone(self):
        return self.phone
    
"""
Class representing a person, should have a attribute representing the 
list of services that customer can offer
"""
class Employee(Person):
    def __init__(self, first_name, last_name, phone_num):
        super().__init__(first_name, last_name, phone_num)
        self.customers = []

        with open("./Pickle/employees.pickle", "rb+") as path:
            elist = pickle.load(path)
            path.truncate()
            path.seek(0)
            elist.append(self)
            pickle.dump(elist, path)

    def __eq__(self, other):
        return super().__eq__(other)
    
    def addCustomer(self, customer):
        assert isinstance(customer, Customer)
        self.customers.append(customer)

    def removeCustomer(self, customer):
        assert isinstance(customer, Customer)
        self.customers.remove(customer)

"""
Class representing a Customer

Will be adding placement attribute to indicate where on the spreadsheet 
this customer is at. This is a workaround as I can't store tkinter frames
in pickles or in dictionaries

For the same reason as the indices, will be adding a services attribute to 
indicate what services this customer wanted
"""
class Customer(Person):
    def __init__(self, first_name, last_name, phone_num):
        super().__init__(first_name, last_name, phone_num)

        self.placement = (0,0)  
        self.selected_services = []

    def __eq__(self, other):
        return super().__eq__(other)

    def setPlacement(self, start, end):
        assert isinstance(start, int) and isinstance(end, int)
        assert end > start
        self.placement = (start, end)

    def getPlacement(self):
        return self.placement

    def getSpan(self):
        return self.placement[1]-self.placement[0]

    def addServices(self, *args):
        if isinstance(args, list): args = args[0]
        # Just to make sure that the service is in the list of services, 
        # will remove once fully implemented to prevent overlap in the pickle (if that is even possible)
        with open("./Pickle/services.pickle", "rb+") as path:
            slist = pickle.load(path)
            for service in args:
                assert isinstance(service, Service)
                slist.index(service)        # Throws ValueError if not in list
        self.selected_services += args
