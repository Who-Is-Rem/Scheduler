from tkinter import *
from tkinter import ttk

# Test

"""
The basic grid that will be used by a subclass SpreadSheet

The rf is the row factor which is the number of cell division there should be 
in each cell, this is to allow more dynamic placement of widgets later on in 
the cells. If the row factor is one then the cell would just be one whole cell.
If the row factor is 2 then the cell would be divided into two halves, etc.
Same idea with cf--the column factor.
"""
class Grid(ttk.Frame):
    """
    Should initialize with m rows and n columns. Columns and rows DO NOT represent 
    the grid's number of rows and columns but the visual columns and rows created 
    by the seprators.

    The separators should be in the even numbered grid columns and grid rows. While
    the "cells" would occupy the odd numbered grids.

    n,m >= 1
    """
    def __init__(self, parent, cols=1, rows=1, rf=1, cf=1):
        assert cols >= 1 and rows >= 1
        self.cols = IntVar(value=cols)
        self.rows = IntVar(value=rows)
        self.row_factor = rf+1
        self.column_factor = cf+1
        ttk.Frame.__init__(self, parent)  

        # ===== Initialize basic grid configs =====
        self.grid_columnconfigure(list(range(1,self.getColSpan(), 2)), uniform="cols",weight=1)
        self.grid_rowconfigure(list(range(1, self.getRowSpan(), 2)), uniform="rows",weight=1)

        # ===== Create the grid =====
        for i in range(cols+1):
            self.makeColSep(i)
        for i in range(rows+1):
            self.makeRowSep(i)

    def getColSpan(self):
        return (self.getColumnFactor()*self.cols.get())+1
    
    def getRowSpan(self):
        return (self.getRowFactor()*self.rows.get())+1
    
    def getRowFactor(self):
        return self.row_factor
    
    def getColumnFactor(self):
        return self.column_factor

    """
    Has a custom event to detect when the number of rows are changed
    """
    def makeColSep(self, c):
        sep = ttk.Separator(self, orient="vertical")
        sep.grid(row=0, column=(c*self.getColumnFactor()), rowspan=self.getRowSpan(), sticky="nsew")
        self.bind("<<RowChange>>", lambda e, sep=sep: sep.grid(row=0, column=(c*self.getColumnFactor()), rowspan=self.getRowSpan(), sticky="nsew"), add="+")

    """
    Has a custom event to detect when the number of columns are changed
    """
    def makeRowSep(self, r):
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=(r*self.getRowFactor()), column=0, columnspan=self.getColSpan(), sticky="nsew")
        self.bind("<<ColumnChange>>", lambda e, sep=sep: sep.grid(row=(r*self.getRowFactor()), column=0, columnspan=self.getColSpan(), sticky="nsew"), add="+")
        
"""
A subclass of GridData that can accept a command to add or remove a row/column
"""
class SpreadSheet(Grid):
    def __init__(self, parent, cols, rows, rf=3):       # setting default row factor to 3 as that is the number of divisions I have in mind for this scheduler
        super().__init__(parent, cols, rows, rf)

        # Grid configure such that every fourth row and column has weight of zero
        self.grid_columnconfigure(list(range(self.getColSpan())), uniform="cols",weight=1)
        self.grid_columnconfigure(list(range(0,self.getColSpan(), self.getColumnFactor())),weight=0)
        self.grid_rowconfigure(list(range(self.getRowSpan())), uniform="rows",weight=1)
        self.grid_rowconfigure(list(range(0,self.getRowSpan(), self.getRowFactor())),weight=0)

        # ===== Trace Functionality =====
        self.cols.trace("w", lambda *args: [
            self.grid_columnconfigure(list(range(self.getColSpan())), uniform="cols",weight=1),
            self.grid_columnconfigure(list(range(0,self.getColSpan(), self.getColumnFactor())),weight=0),
            self.makeColSep(self.cols.get()),
            self.event_generate("<<ColumnChange>>")
            ])
        self.rows.trace("w", lambda *args: [
            self.grid_rowconfigure(list(range(self.getRowSpan())), uniform="rows",weight=1),
            self.grid_rowconfigure(list(range(0,self.getRowSpan(), self.getRowFactor())),weight=0),
            self.makeRowSep(self.rows.get()),
            self.event_generate("<<RowChange>>")
            ])

    """
    Simply add 1 to self.cols and let a IntVar.trace handle expansion
    """
    def add_column(self):
        self.cols.set(self.cols.get()+1)

    """
    Simply add 1 to self.rows and let a IntVar.trace handle expansion
    """
    def add_row(self):
        self.rows.set(self.rows.get()+1)
        
"""
Now this will be the actual SpreadSheet that will be used in my scheduler
Will be abusing the fact that I can use grid row 0 to put in employee labels
and grid column 0 to put labels for time

The employee labels should not interact with column 0
The time labels should not interact with row 0
"""
class ScheduleSheet(SpreadSheet):
    def __init__(self, parent, cols, rows, rf=3):
        super().__init__(parent, cols, rows, rf)
        