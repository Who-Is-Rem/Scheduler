from CustomTime import *
import numpy as np

"""
A matrix of time where rows will represent the time segments and the 
columns will represent from where the data is being collected

A 1 represents the time segment being taken and a 0 represents the 
time segment being empty

e.g. rows of 15min intervals and each column representing an employee
     thus, a simplified schedule of employees with numbers

custom_time should be a CustomTime object and tdiv should be an int of 
multiple 5

custom_time and tdiv should not be accessible with get methods
"""
class TimeMatrix():
    def __init__(self, custom_time, tdiv):
        assert isinstance(custom_time, CustomTime) and isinstance(tdiv, int)
        assert tdiv%5==0
        self.DT = 'int8'
        self.ct = custom_time
        self.tdiv = tdiv
        self.matrix = np.zeros((custom_time.getTotalMinutes()//tdiv, 0), dtype=self.DT)

    def addColumn(self):
        tmp = np.zeros((self.ct.getTotalMinutes()//self.tdiv, 1), dtype=self.DT)
        self.matrix = np.hstack((self.getMatrix(), tmp))

    def getMatrix(self):
        return self.matrix
    
    def getSize(self):
        return self.getMatrix().shape

    def getSegment(self, column, start, end):
        assert isinstance(column, int) and isinstance(start, int) and isinstance(end, int)
        assert column >=0 and start >=0
        if end == -1: end = self.getMatrix().shape[0]
        return self.getMatrix()[start:end, column]
    
"""
Matrix of time for the spreadsheet to keep track of where customers are in each 
employee column
"""
class SpreadSheetMatrix(TimeMatrix):
    def __init__(self, custom_time, tdiv):
        super().__init__(custom_time, tdiv)

    """
    Checks the avaliablity of the rows in some column from some start entry 
    to some end entry
    """
    def checkAvailable(self, column, start, end):
        assert isinstance(end, int) and isinstance(start, int) and isinstance(column, int) and end > start
        seg = self.getSegment(column, start, end).copy()
        print(seg)
        one = np.ones(seg.shape, self.DT)
        seg += one
        if seg.max()<=1:
            return True
        return False
    
    """
    Returns false if failing to occupy some space and returns true if the space can and is now occupied
    """
    def occupySpace(self, column, start, end):
        assert isinstance(end, int) and isinstance(start, int) and isinstance(column, int) and end > start
        if self.checkAvailable(column, start, end):
            self.matrix[start:end, column] = 1
            return True
        return False
    
    """
    Removes all occupied spaces, i.e. 1, from some column in a matrix from the start entry to the end entry

    Returns True if invariant is passed and all entries are zeroed else False

    Invariant: All entries from start to end MUST be occupied, i.e. 1
    """
    def removeSpace(self, column, start, end):
        ms = self.getSegment(column, start, end).copy()
        print(ms)
        if ms.min() == 1:
            self.matrix[start:end, column] = 0
            return True
        return False
