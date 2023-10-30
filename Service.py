from CustomTime import *

"""
Class representing a Service.

Should expect strings as the input for the initializer
"""
class Service():
    def __init__(self, name, price, esttime, maxtime, short):
        assert isinstance(name, str) and isinstance(esttime, str) and isinstance(maxtime, str)
        assert isinstance(int(price), int)
        self.name = " ".join(list(map(lambda s: s[0].upper()+s[1:], name.split(" "))))
        self.price = int(price)
        self.time_range = ServiceTimeRange(esttime, maxtime)
        self.short = short

    def __eq__(self, other):
        assert isinstance(other, Service)
        return self.toString()==other.toString()
    
    def getShort(self):
        return self.short

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
    
    def addAll(self, *args):
        if isinstance(args[0], list): 
            args = args[0]
            for service in args: assert isinstance(service, Service)
        total_time = self.time_range.addAll(args)
        total_price = 0
        for service in args: total_price += service.getPrice()
        return total_price, total_time