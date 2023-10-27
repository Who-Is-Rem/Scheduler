"""
Class that represent time in military time

If no specific time is given set the time to 00:00
The minimum is 00:00 and the maximum is 23:59
"""
class CustomTime():
    def __init__(self, hr=0, min=0):
        assert hr>=0 and hr <24
        assert min>=0 and min <60
        self.hour = hr
        self.min = min

    def __eq__(self, other):
        assert isinstance(other, CustomTime)
        return (self.getHour()==other.getHour()) and (self.getMin()==other.getMin())

    def getHour(self):
        return self.hour
    
    def getMin(self):
        return self.min

    """
    Adds some amopunt of time to the current time and returns a new CustomTime Object
    """
    def addTime(self, dhours=0, dmins=0):
        assert dhours>=0 and dmins >= 0
        if self.min+dmins<60:
            tmin = self.min+dmins 
        else: 
            tmin = (self.min+dmins)%60 
            dhours+=(self.min+dmins)//60
        thours = self.hour+dhours if self.hour+dhours<24 else (self.hour+dhours)%24
        return CustomTime(thours,tmin)

    def toString(self):
        return f"{"0" if self.getHour()<10 else ""}{self.getHour()}:{"0" if self.getMin()<10 else ""}{self.getMin()}"

"""
A Time class that will be used for displaying the time for the spreadsheet
"""
class SheetTime(CustomTime):
    def __init__(self, hr, min):
        super().__init__(hr, min)

    def __eq__(self, other):
        return super().__eq__(other)

    def addTime(self, dhours=0, dmins=0):
        assert dmins%15==0
        return super().addTime(dhours, dmins)
    
class ServiceTime(CustomTime):
    def __init__(self, hr, min):
        super().__init__(hr, min)

    def __eq__(self, other):
        return super().__eq__(other)

    def addTime(self, dhours=0, dmins=0):
        assert dmins%5==0
        ct = super().addTime(dhours, dmins)
        return ServiceTime(ct.getHour(), ct.getMin())

    def toString(self):
        return f"{self.getHour()}h{self.getMin()}m"
    
    def getCopy(self):
        return self

    """
    Returns the total time it takes for some number of services including the current service
    """
    def addAll(self, *args):
        # For when the addAll function in ServiceTimeRange is used
        if isinstance(args[0], list): args = args[0]
        for arg in args:
            assert isinstance(arg, ServiceTime)
        tmp = self.getCopy()
        for a in args:
            tmp = tmp.addTime(a.getHour(), a.getMin()) 
        return tmp
    
"""
A function that will convert a string representation of time to 
a tuple of hours and minutes. Time should be in 24hr format.
This function essentially reverses the toString() method in 
the ServiceTime class

Sting should be in the format of --h--m

e.g. 0h10m -> (0, 10)
"""
def StringToServiceTime(string):
    assert isinstance(string, str)
    assert len(string)>=4
    hindex = string.find("h")
    mindex = string.find("m")
    assert hindex != -1 and mindex != -1 and mindex == (len(string)-1)
    return ServiceTime(int(string[0:hindex]), int(string[hindex+1:mindex]))

"""
Class for displaying the range of time a service may take. THe maximum time 
should be greater than the estimated time

e.g. A Manicure may take 30-35 minutes
"""
class ServiceTimeRange():
    def __init__(self, estimate="0h0m", max="0h0m"):
        assert isinstance(estimate, str) and isinstance(max, str)
        
        self.max = StringToServiceTime(max)
        self.estimate = StringToServiceTime(estimate)
        hdiff = self.max.getHour()-self.estimate.getHour()
        mdiff = self.max.getMin()-self.estimate.getMin()
        assert hdiff>0 or (hdiff==0 and mdiff>=0)
        self.difference = ServiceTime(hdiff, mdiff)

    def __eq__(self, other):
        assert isinstance(other , ServiceTimeRange)
        return (self.getMax()==other.getMax()) and (self.getEstimate()==other.getEstimate()) 

    def getEstimate(self):
        return self.estimate
    
    def getMax(self):
        return self.max
    
    def getDifference(self):
        return self.difference
    
    def toString(self):
        return (f"Estimate: {self.getEstimate().toString()}\nMax: {self.getMax().toString()}\n"+
                f"Difference: {self.getDifference().toString()}")

    def addAll(self, *args):
        for arg in args:
            assert isinstance(arg, ServiceTimeRange)
        etmp = self.estimate.addAll(list(map(lambda arg: arg.getEstimate(), args)))
        mtmp = self.max.addAll(list(map(lambda arg: arg.getMax(), args)))
        return ServiceTimeRange(etmp.toString(), mtmp.toString())
    



