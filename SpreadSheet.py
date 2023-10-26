from tkinter import *
from tkinter import ttk

"""
A class that creates a spread sheet frame, should be equally sized grids 
in both direction and fill the entire parent frame, which would be the 
root window when testing.
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
    def __init__(self, parent, cols=1, rows=1):
        assert cols >= 1 and rows >= 1

        # ===== Initialize basic atributes =====
        self.cols = IntVar(value=cols)
        self.rows = IntVar(value=rows)
        self.colSpan = (cols*2)+1
        self.rowSpan = (rows*2)+1


        # ===== Initialize basic grid configs =====
        ttk.Frame.__init__(self, parent)   
        self.grid_columnconfigure(list(range(1,self.getColSpan(), 2)), uniform="cols",weight=1)
        self.grid_rowconfigure(list(range(1, self.getRowSpan(), 2)), uniform="rows",weight=1)

        # ===== Create the grid =====
        for i in range(cols+1):
            self.makeColSep(i)
        for i in range(rows+1):
            self.makeRowSep(i)

    """
    Has a custom event to detect when the number of rows are changed
    """
    def makeColSep(self, c):
        sep = ttk.Separator(self, orient="vertical")
        sep.grid(row=0, column=(c*2), rowspan=self.getRowSpan(), sticky="nsew")
        self.bind("<<RowChange>>", lambda e, sep=sep: sep.grid(row=0, column=(c*2), rowspan=self.getRowSpan(), sticky="nsew"), add="+")

    """
    Has a custom event to detect when the number of columns are changed
    """
    def makeRowSep(self, r):
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=(r*2), column=0, columnspan=self.getColSpan(), sticky="nsew")
        self.bind("<<ColumnChange>>", lambda e, sep=sep: sep.grid(row=(r*2), column=0, columnspan=self.getColSpan(), sticky="nsew"), add="+")

    def getColSpan(self):
        return (self.cols.get()*2)+1
    
    def getRowSpan(self):
        return (self.rows.get()*2)+1

"""
A subclass of Grid that can accept a command to add or remove a row/column
"""
class SpreadSheet(Grid):
    def __init__(self, parent, cols, rows):
        super().__init__(parent, cols, rows)

        # ===== Trace Functionality =====
        self.cols.trace("w", lambda *args: [
            self.grid_columnconfigure(list(range(1,self.getColSpan(), 2)), uniform="cols",weight=1),
            self.makeColSep(self.cols.get()),
            self.event_generate("<<ColumnChange>>")
            ])
        self.rows.trace("w", lambda *args: [
            self.grid_rowconfigure(list(range(1,self.getRowSpan(), 2)), uniform="rows",weight=1),
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
        
