from tkinter import *
from tkinter import ttk

"""
A class taht creates a spread sheet frame, should be equally sized grids 
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
        self.cols = cols
        self.rows = rows
        self.grid_cols = (cols*2)+1
        self.grid_rows = (rows*2)+1


        # ===== Initialize basic grid configs =====
        ttk.Frame.__init__(self, parent)   
        self.grid_columnconfigure(list(range(1,self.grid_cols, 2)), uniform="cols",weight=1)
        self.grid_rowconfigure(list(range(1, self.grid_rows, 2)), uniform="rows",weight=1)

        # ===== Create the grid =====
        for i in range(cols+1):
            sep = ttk.Separator(self, orient="vertical")
            sep.grid(row=0, column=(i*2), rowspan=self.grid_rows, sticky="nsew")
            self.bind("<Configure>", lambda sep=sep: sep.grid(row=0, column=(i*2), rowspan=self.getRowSpan(), sticky="nsew"), add="+")
        for i in range(rows+1):
            sep = ttk.Separator(self, orient="horizontal")
            sep.grid(row=(i*2), column=0, columnspan=self.grid_cols, sticky="nsew")
            self.bind("<Configure>", lambda sep=sep: sep.grid(row=(i*2), column=0, columnspan=self.getColSpan(), sticky="nsew"), add="+")

    def getColSpan(self):
        return self.grid_cols
    
    def getRowSpan(self):
        return self.grid_rows
