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
        self.services = []

        with open("./Pickle/employees.pickle", "rb+") as path:
            elist = pickle.load(path)
            path.truncate()
            path.seek(0)
            elist.append(self)
            pickle.dump(elist, path)

    def __eq__(self, other):
        return super().__eq__(other)

    def addService(self, service):
        with open("./Pickle/services.pickle", "rb+") as path:
            slist = pickle.load(path)
            slist.index(service)        # Will throw a ValueError if service is not in the list
        self.services.append(service)


"""
Class representing a person 
"""
class Customer(Person):
    def __init__(self, first_name, last_name, phone_num):
        super().__init__(first_name, last_name, phone_num)

    def __eq__(self, other):
        return super().__eq__(other)

