from tkinter import *
from tkinter import ttk
from CustomTime import *
from People import *

"""
The basic grid setup that will be used by a subclass SpreadSheet

The rf is the row factor which is the number of cell division there should be 
in each cell, this is to allow more dynamic placement of widgets later on in 
the cells. If the row factor is one then the cell would just be one whole cell.
If the row factor is 2 then the cell would be divided into two halves, etc.
Same idea with cf--the column factor.
"""
class GridSetUp(ttk.Frame):
    """
    Columns and rows DO NOT represent the grid's number of rows and columns but the 
    visual columns and rows created by the seprators.

    The separators should be in the even numbered grid columns and grid rows. While
    the "cells" would occupy the odd numbered grids.

    n,m >= 1
    """
    def __init__(self, parent, cols=0, rows=1, rf=1, cf=1):
        assert cols >= 0 and rows >= 0
        self.parent = parent
        self.cols = IntVar(value=cols)
        self.rows = IntVar(value=rows)
        self.row_factor = rf+1
        self.column_factor = cf+1
        ttk.Frame.__init__(self, parent)  
        self.grid_propagate(False)

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
        sep.grid(row=(r*self.getRowFactor()), column=0, columnspan=self.getColSpan(), sticky="sew")
        self.bind("<<ColumnChange>>", lambda e, sep=sep: sep.grid(row=(r*self.getRowFactor()), column=0, columnspan=self.getColSpan(), sticky="nsew"), add="+")
        
"""
A subclass of GridData that can accept a command to add or remove a row/column
"""
class SpreadSheet(GridSetUp):
    def __init__(self, parent, cols=0, rows=1, rf=3):       # setting default row factor to 3 as that is the number of divisions I have in mind for this scheduler
        super().__init__(parent, cols, rows, rf)
        self.minW = 200
        self.minH = 10
        if cols>0:
            self.grid_columnconfigure(list(filter(lambda i: i%self.getColumnFactor()!=0, list(range(self.getColSpan())))), 
                                  weight=1, uniform="cols", minsize=self.minW)
        if rows>0:
            self.grid_rowconfigure(list(filter(lambda i: i%self.getRowFactor()!=0, list(range(self.getRowSpan())))), 
                                  weight=1, uniform="rows", minsize=self.minH)
            
        # ===== Create the grid =====
        for i in range(cols+1):
            self.makeColSep(i)
        for i in range(1, rows+1):
            self.makeRowSep(i)

        # ===== Trace Functionality =====
        self.cols.trace("w", lambda *args: [
            self.grid_columnconfigure(list(filter(lambda i: i%self.getColumnFactor()!=0, list(range(self.getColSpan())))), 
                                  weight=1, uniform="cols", minsize=self.minW),
            self.makeColSep(self.cols.get()),
            self.event_generate("<<ColumnChange>>"), self.event_generate("<<SizeChange>>")
            ])
        self.rows.trace("w", lambda *args: [
            self.grid_rowconfigure(list(filter(lambda i: i%self.getRowFactor()!=0, list(range(self.getRowSpan())))), 
                                  weight=1, uniform="rows", minsize=self.minH),
            self.makeRowSep(self.rows.get()),
            self.event_generate("<<RowChange>>"), self.event_generate("<<SizeChange>>"),
            ])
        
        self.bind("<<SizeChange>>", lambda e: self.configure(
            width=self.parent.winfo_width() if self.minW*self.cols.get()*(self.getColumnFactor()-1)<self.parent.winfo_width() else self.minW*self.cols.get()*(self.getColumnFactor()-1), 
            height=self.parent.winfo_height() if self.minH*self.rows.get()*(self.getRowFactor()-1)<self.parent.winfo_height() else self.minH*self.rows.get()*(self.getRowFactor()-1)))

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
The SchedulerSheet class is the spread sheet that will be used in the scheduler. Should have a 
Dictionary of column numbers and the widgets contained in each column; these columns are the
columns of the spreadsheet not the grid columns

The Scheduler time will range from 8am to 8pm with is from 08:00 to 20:00 for a total of 12hrs
or 720 minutes. Each segment should be 15 minutes so there will be 720//15 rows i.e. 48

May have to implement a "margin" of sorts at the bottom of the spreadsheet to show 20:00
Initially will not utilize employees.pickle but will later. Currently, no employees exist

The Employee names SHOULD NOT use columns 0
"""
class SchedulerSheetCanvas(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = Canvas(self, highlightthickness=0, bg = "yellow")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.employee_frame = ttk.Frame(self, height=40)
        self.employee_id = self.canvas.create_window((0,0), window=self.employee_frame, anchor=NW)

        self.spread_sheet = SpreadSheet(self.canvas, cols=0, rows=48, rf=3)
        self.ssframe_id = self.canvas.create_window((0,40),window=self.spread_sheet, anchor=NW, tags="scroll")
        self.canvas.configure(scrollregion=(0, 0)+self.canvas.bbox("scroll")[2:])
        self.spread_sheet.bind("<<SizeChange>>", lambda e: [self.canvas.configure(scrollregion=(0, 0)+self.canvas.bbox("scroll")[2:],
                                                                                  height=self.spread_sheet.winfo_height(),
                                                                                  width=self.spread_sheet.winfo_width())], add="+")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1*(e.delta), "units") if e.state==0 else self.canvas.xview_scroll(-1*(e.delta), "units")) 

    def addEmployee(self, employee):
        # assert isinstance(employee, Employee)     # Haven't fully implemented employees so will comment out
        # TODO: process employee data and assign appropriate name
        empLabel = LabelFrame(self, text=employee)

