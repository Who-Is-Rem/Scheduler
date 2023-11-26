from tkinter import *
from tkinter import ttk
from CustomTime import *
from People import *
from TimeMatrix import *
from CustomerFrame import *

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
        self.cols = cols
        self.rows = rows
        self.row_factor = rf+1
        self.column_factor = cf+1
        ttk.Frame.__init__(self, parent)  
        self.grid_propagate(False)

    def getColSpan(self):
        return (self.getColumnFactor()*self.cols)+1
    
    def getRowSpan(self):
        return (self.getRowFactor()*self.rows)+1
    
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
        self.minW = 100
        self.minH = 10
        if cols>0:
            self.grid_columnconfigure(list(filter(lambda i: i%self.getColumnFactor()!=0, list(range(self.getColSpan())))), 
                                  weight=1, uniform="cols", minsize=self.minW)
        if rows>0:
            self.grid_rowconfigure(list(filter(lambda i: i%self.getRowFactor()!=0, list(range(self.getRowSpan())))), 
                                  weight=2, uniform="rows", minsize=self.minH)
            
        # ===== Create the grid =====
        for i in range(cols+1):
            self.makeColSep(i)
        for i in range(1, rows):        # Originally (rows+1), but was changed to fit aesthetics
            self.makeRowSep(i)

        self.bind("<<SizeChange>>", lambda e: self.configure(
            width=self.parent.winfo_width() if self.minW*self.cols*self.getColumnFactor()<self.parent.winfo_width() else self.minW*self.cols*self.getColumnFactor(), 
            height=self.parent.winfo_height() if self.minH*self.rows*self.getRowFactor()<self.parent.winfo_height() else self.minH*self.rows*self.getRowFactor()))

    """
    Helper function that should be called upon to create new columns

    Does not include initialized columns
    """
    def add_column(self):
        self.cols += 1
        self.grid_columnconfigure(list(filter(lambda i: i%self.getColumnFactor()!=0, list(range(self.getColSpan())))), 
                                weight=1, uniform="cols", minsize=self.minW)
        self.makeColSep(self.cols)
        self.event_generate("<<ColumnChange>>") 
        self.event_generate("<<SizeChange>>")

    """
    Helper function that should be called upon to create new rows

    Does not include initialized rows
    """
    def add_row(self):
        self.rows += 1
        self.grid_rowconfigure(list(filter(lambda i: i%self.getRowFactor()!=0, list(range(self.getRowSpan())))), 
                                weight=2, uniform="rows", minsize=self.minH)
        self.makeRowSep(self.rows)
        self.event_generate("<<SizeChange>>")
        self.event_generate("<<RowChange>>")

class ScrollableSpreadSheet(Frame):
    def __init__(self, parent):
        self.time_matrix = SpreadSheetMatrix(CustomTime(12), 5)

        Frame.__init__(self, parent)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.ss_canvas = Canvas(self, highlightthickness=0, bg = "white")
        self.ss_canvas.grid(row=1, column=1, sticky="nsew")
        self.ss_canvas.parent = self

        self.spread_sheet = SpreadSheet(self.ss_canvas, cols=0, rows=48, rf=3)
        self.ssframe_id = self.ss_canvas.create_window((0,0),window=self.spread_sheet, anchor=NW, tags="spreadsheet")

        self.ss_canvas.configure(scrollregion=self.ss_canvas.bbox("all"))

        self.ss_canvas.bind("<Configure>", lambda e: self.spread_sheet.event_generate("<<SizeChange>>"))
        self.spread_sheet.bind("<<SizeChange>>", lambda e: self.ss_canvas.configure(scrollregion=self.ss_canvas.bbox("all"),
                                                                                     width=self.spread_sheet.winfo_width()), 
                                                            add="+")
        self.bind_all("<MouseWheel>", lambda e: self.ss_canvas.yview_scroll(-1*(e.delta), "units")
                                                if e.state==0 
                                                else self.ss_canvas.xview_scroll(-1*(e.delta), "units")) 

class SchedulerSheet(ScrollableSpreadSheet):
    def __init__(self, parent):
        super().__init__(parent)
        tmpf = ttk.Frame(self)
        tmpf.grid(column=0, row=0, rowspan=2, sticky="nsew")
        tmpf.grid_columnconfigure(0, weight=1)
        tmpf.grid_rowconfigure(0, weight=1)

        self.queue = ttk.Frame(tmpf, style="queue.TFrame", name="queue")
        self.queue.grid(column=0, row=0, sticky="nsew")
        Frame(self.queue).pack(side=BOTTOM)

        self.spread_sheet.grid_rowconfigure([0, 192], weight=1)
        l1 = Label(self.spread_sheet,text="", font=("Helvetica", 5))
        l1.grid(column=1, row=0, sticky="nsew", columnspan=self.spread_sheet.getColSpan())
        l2 = Label(self.spread_sheet,text="", font=("Helvetica", 5))
        l2.grid(column=1, row=192, sticky="nsew", columnspan=self.spread_sheet.getColSpan())
        self.spread_sheet.bind("<<ColumnChange>>", lambda e: [l1.grid(columnspan=self.spread_sheet.getColSpan()),
                                                              l2.grid(columnspan=self.spread_sheet.getColSpan())], 
                                                              add="+")

        self.emp_canvas = Canvas(self, highlightthickness=0, bg = "yellow", height=40)
        self.emp_canvas.grid(row=0, column=1, sticky="nsew")

        self.spread_sheet.grid_propagate(False)
        self.employees_frame = ttk.Frame(self.emp_canvas, style="Employee.TFrame")
        self.employees_frame.grid_propagate(False)
        self.empframe_id = self.emp_canvas.create_window((0,0), window=self.employees_frame, anchor=NW)
        self.emp_canvas.configure(scrollregion=self.emp_canvas.bbox("all"))

        self.spread_sheet.bind("<<SizeChange>>", lambda e: 
                               [self.employees_frame.configure(width=self.spread_sheet.winfo_width(), height=40),
                                self.emp_canvas.configure(
                                   scrollregion=self.emp_canvas.bbox("all"),
                                   height=40,
                                   width=self.spread_sheet.winfo_width())],
                                add="+")
        self.bind_all("<MouseWheel>", lambda e: self.emp_canvas.xview_scroll(-1*(e.delta), "units") if e.state == 1 else NONE, add="+")

    def addEmployee(self, employee=NONE):
        #TODO: implement proper addition of a employee Label
        self.spread_sheet.add_column()
        current_length = len(self.employees_frame.winfo_children())
        self.employees_frame.grid_columnconfigure(current_length, weight=1, uniform="emp")
        
        # ===== TEMPORARY FOR TESTING =====

        ename = ttk.Label(self.employees_frame,text=f"{len(self.employees_frame.winfo_children())}", 
                          name=f"{current_length}",
                          anchor=CENTER,
                          style="Employee.TLabelframe.Label")
        ename.grid(row=0, column=current_length, sticky="nsew")

        # =================================

    def addCustomer(self, customer=Customer("test", "testing", "1234567890")):
        customerFrame = CustomerFrame(self.spread_sheet, self.queue, customer,[Service("Foo", "15", "1h0m", "1h0m", "FO"), Service("Poopy", "15", "0h30m", "0h30m", "P")])
        customerFrame.pack(in_=self.queue)
        