from CustomTime import *

"""
Class representing a Service.

Should expect strings as the input for the initializer
"""
class Service():
    def __init__(self, name, price, esttime, maxtime):
        assert isinstance(name, str) and isinstance(esttime, str) and isinstance(maxtime, str)
        assert isinstance(int(price), int)
        self.name = " ".join(list(map(lambda s: s[0].upper()+s[1:], name.split(" "))))
        self.price = int(price)
        self.time_range = ServiceTimeRange(esttime, maxtime)

    def __eq__(self, other):
        assert isinstance(other, Service)
        return self.toString()==other.toString()

    def toString(self):
        return self.name
    
    def getPrice(self):
        return self.price
    
    def getEstimatedTime(self):
        return self.time_range.getEstimate().toString()
    
    def getMaxTime(self):
        return self.time_range.getMax().toString()
    
    def getDifferenceTime(self):
        return self.time_range.getDifference().toString()