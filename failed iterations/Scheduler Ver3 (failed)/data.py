"""
Classes pertaining to the information of people, such as
Empoyees and Customers, and services
"""

class DataRange():
    def __init__(self, min, max=0):
        assert isinstance(min, int)
        assert isinstance(max, int)
        assert min >= 0 and max >= 0

        # ===== Basic Attributes =====
        self.min = min
        if max == 0:
            self.max = self.min
        else:
            self.max = max

    def __eq__(self, obj):
        try: 
            assert isinstance(obj, DataRange)
            assert self.min == obj.getMin()
            assert self.max == obj.getMax()
            assert self.getString() == obj.getString()
            return True
        except: return False

    def add(self, obj):
        assert isinstance(obj, DataRange)
        return DataRange(self.min+obj.min, self.max+obj.max)

    def getMin(self):
        return self.min
    
    def getMax(self):
        return self.max
        
    def add(self, obj):
        return DataRange(self.min+obj.min, self.max+obj.max)
    
    def getString(self):
        return str(self.min) if self.min == self.max else f"{self.min}-{self.max}"

class Service():
    def __init__(self, name, abbrev, price_range, time_range):
        assert isinstance(price_range, str)
        assert isinstance(time_range, str)

        # ===== Basic Attributes =====
        self.name = name.strip().capitalize()
        self.short_name = abbrev.strip().capitalize()

        pl = price_range.strip().split("-")
        tl = time_range.strip().split("-")
        self.price = DataRange(int(pl[0]), int(pl[1])) if len(pl) == 2 else DataRange(int(pl[0]))
        self.time = DataRange(int(tl[0]), int(tl[1])) if len(tl) == 2 else DataRange(int(tl[0]))

        assert self.time.getMin()%5==0
        assert self.time.getMax()%5==0

    def __eq__(self, obj):
        try: 
            assert isinstance(obj, Service)
            assert self.getName() == obj.getName()
            assert self.getShort() == obj.getShort()
            return True
        except: return False

    def getName(self):
        return self.name
    
    def getShort(self):
        return self.short_name
    
    def getPrice(self):
        return self.price
    
    def getTime(self):
        return self.time
    
class Employee():
    def __init__(self, fname, lname, number):
        assert isinstance(fname, str)
        assert isinstance(lname, str)
        assert isinstance(number, str)
        assert len(number) == 10

        # ===== Basic Attributes =====
        self.first_name = fname.strip().capitalize()
        self.last_name = lname.strip().capitalize()
        self.number = number

        self.customers = []

    def __eq__(self, obj):
        try: 
            assert isinstance(obj, Employee)
            assert self.getName() == obj.getName()
            assert self.getFullName() == obj.getFullName()
            assert self.getNumber() == obj.getNumber()
            return True
        except: return False

    def addCustomer(self, cust):
        assert isinstance(cust, Customer)
        self.customers.append(cust)

    def removeCustomer(self, cust):
        assert isinstance(cust, Customer)
        assert cust in self.getCustomers()
        self.customers.remove(cust)

    def getFullName(self):
        return f"{self.first_name} {self.last_name}"
    
    def getName(self):
        return self.first_name
    
    def getNumber(self):
        return self.number

    def getCustomers(self):
        return self.customers
    
class Customer():
    def __init__(self, fname, lname, number, services=[]):
        assert isinstance(fname, str)
        assert isinstance(lname, str)
        assert isinstance(number, str)
        assert len(number) == 10
        for s in services:
            assert isinstance(s, Service)

        # ===== Basic Attributes =====
        self.first_name = fname.strip().capitalize()
        self.last_name = lname.strip().capitalize()
        self.number = number.strip()
        self.services = services

        # ===== For Frames =====
        self.served = False
        self.locked = False
        self.row = None

    def __eq__(self, obj):
        try: 
            assert isinstance(obj, Customer)
            assert self.getName() == obj.getName()
            assert self.getFullName() == obj.getFullName()
            assert self.getServices() == obj.getServices()
            assert self.getNumber() == obj.getNumber()
            
            return True
        except: return False

    def setServed(self, boolean):
        assert isinstance(boolean, bool)
        self.served = boolean

    def setLocked(self, boolean):
        assert isinstance(boolean, bool)
        self.locked = boolean

    def lockToggle(self):
        self.locked = not self.locked

    def getServed(self):
        return self.served
    
    def getLocked(self):
        return self.locked

    def getFullName(self):
        return f"{self.first_name} {self.last_name}"
    
    def getName(self):
        return self.first_name
    
    def getLastNameShort(self):
        return f"{self.last_name[0]}."
    
    def getNumber(self):
        return self.number
    
    def getServices(self):
        return self.services
