import pickle
from tkinter import messagebox

class Approx():
    def __init__(self, entryStr):
        values = entryStr.strip().split("-")
        min = int(values[0])
        max = int(values[1]) if len(values)==2 else min
        assert isinstance(min, int)
        assert isinstance(max, int)
        assert min >= 0
        assert max >= min
        self.min = min
        self.max = max

    def getString(self):
        if self.min != self.max:
            return f"{self.min}-{self.max}"
        return f"{self.min}"

    def getMin(self):
        return self.min
    
    def getMax(self):
        return self.max
    
    def getApproxRange(self):
        return str(self.min) if self.min == self.max else f"{self.min}-{self.max}"
    
    def __eq__(self, obj):
        try:
            assert self.min == obj.min
            assert self.max == obj.max
            assert self.getApproxRange() == obj.getApproxRange()
            return True
        except:
            return False
    
class PriceRange(Approx):
    def __init__(self, entryStr):
        super().__init__(entryStr)
    
    def add(self, obj):
        assert isinstance(obj, PriceRange)
        approxMin = self.min + obj.min
        approxMax = self.max + obj.max
        return PriceRange(f"{approxMin}-{approxMax}")

class TimeRange(Approx):
    def __init__(self, entryStr):
        super().__init__(entryStr)
        assert (self.min%15 == 0) 
        assert (self.max%15 == 0)

    def add(self, obj):
        assert isinstance(obj, TimeRange)
        approxMin = self.min + obj.min
        approxMax = self.max + obj.max
        return TimeRange(f"{approxMin}-{approxMax}")

class Service():
    def __init__(self, nameOfService, priceRange, timeRange, abbreviation):
        assert len(nameOfService) > 0
        assert len(abbreviation) > 0
        assert isinstance(nameOfService, str)
        assert isinstance(abbreviation, str)
        assert isinstance(priceRange, PriceRange)
        assert isinstance(timeRange, TimeRange)
        nameOfService = " ".join([word.replace(word[0], word[0].upper(), 1) for word in nameOfService.strip().split(" ")])
        self.name = nameOfService
        self.price = priceRange
        self.time = timeRange
        self.shortName = abbreviation

    def getListContent(self):
        return self.getName()

    def getName(self):
        return self.name
    
    def getPrice(self):
        return self.price
    
    def getTime(self):
        return self.time
    
    def getShortName(self):
        return self.shortName

    def __eq__(self, obj):
        try:
            assert isinstance(obj, Service)
            assert self.getName() == obj.getName()
            assert self.getPrice() == obj.getPrice()
            assert self.getTime() == obj.getTime()
            assert self.getShortName().lower() == obj.getShortName().lower()
            return True
        except:
            return False

"""
Instantiates the creation of a person. A super class to customer and employee
"""
class Person():
    """
    Instantiates a person with a first name, last name, and phone number
    """
    def __init__(self, firstName, lastName, phoneNumber):
        assert isinstance(firstName, str)
        assert isinstance(lastName, str)
        assert isinstance(int(phoneNumber), int)
        assert len(phoneNumber) == 10
        assert len(firstName) > 0
        assert len(lastName) >= 0
        self.first_name = firstName.strip().capitalize()
        self.last_name = lastName.strip().capitalize()
        self.pnumber = phoneNumber

    def __eq__(self, obj):
        try:
            assert isinstance(obj, Person)
            assert self.first_name.lower() == obj.first_name.lower()
            assert self.last_name.lower() == obj.last_name.lower()
            assert self.pnumber == obj.pnumber
            return True
        except:
            return False
        
    def getListContent(self):
        return self.getName() + ", " +self.getNumber()

    def getName(self):
        if self.last_name == "":
            return self.first_name
        return self.first_name + " " + self.last_name
    
    def getFirstName(self):
        return self.first_name
    
    def getLastName(self):
        return self.last_name
    
    def getNumber(self):
        return self.pnumber
    
class Employee(Person):
    def __init__(self, firstname, lastname, number):
        super().__init__(firstname, lastname, number)
        self.customers = []

class Customer(Person):
    def __init__(self, firstname, lastname, number, services=[]):
        super().__init__(firstname, lastname, number)
        self.desiredServices = services
        self.row = 0
        self.bg = "red"
        self.locked = False

    def lockToggle(self):
        self.locked = not self.locked

    def setBg(self, color):
        assert isinstance(color, str)
        self.bg = color

    def expectedTime(self):
        t = TimeRange("0")
        for service in self.desiredServices:
            assert isinstance(service, Service)
            t = t.add(service.getTime())
        return t
    
    def expectedPrice(self):
        p = PriceRange("0")
        for service in self.desiredServices:
            assert isinstance(service, Service)
            p = p.add(service.getPrice())
        return p

# This class should NEVER be touched unless resetting the pickle file
# or adding methods to the custom dictionary
class customDict(dict):
    def __init__(self):
        self.keys = ["Employees", "Customers", "Services"]
        self.dictionary = {
            "Employees": [],
            "Customers": [],
            "Services": [],
        }

    def get(self, key):
        assert key in self.keys
        return self.dictionary[key]
    
    def add(self, obj, identifier):
        assert identifier in self.keys
        assert (isinstance(obj, Employee)) or (isinstance(obj, Customer)) or (isinstance(obj, Service))
        with open("./data.pickle", "rb+") as path:
            dict = pickle.load(path)     
            itemList = dict.get(identifier)
            for item in itemList:
                if (item == obj): 
                    messagebox.showerror(title = "Error", message = f"{obj.getName()} is already in the list")
                    break
            else:
                itemList.append(obj)
                path.seek(0)
                path.truncate()
                pickle.dump(dict, path)

    def remove(self, obj, identifier):
        assert identifier in self.keys
        assert (isinstance(obj, Employee)) or (isinstance(obj, Customer)) or (isinstance(obj, Service))
        with open("./data.pickle", "rb+") as path:
            dict = pickle.load(path)
            itemList = dict.get(identifier)
            for item in itemList:
                if item == obj:
                    itemList.remove(item)
                    break
            else:
                messagebox.showerror(title = f"{identifier.capitalize()} Removal Failed", message="Typed Entry is not in the list")
            path.seek(0)
            path.truncate()
            pickle.dump(dict, path)
            
class CustomRemovalError(Exception):
    pass

class CustomAddError(Exception):
    pass
    