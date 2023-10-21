from tkinter import *

# Creation of a Frame with grids in a spreadsheet fashion
# Has two parameters of row and columns
# Height and width can be set via a method if necessary

class SpreadSheet(Frame):
    def __init__(self, master, cols=1, rows=1):
        Frame.__init__(self, master)
        self.grid(row=0,column=0, sticky="nsew")
        self.grid_columnconfigure(list(range(cols)), weight=1)
        self.grid_rowconfigure(list(range(rows)), weight=1)

        # To Keep track of waht widgets are in what column
        self.columnDictionary = {}

    def setColumns(self, col):
        self.grid_columnconfigure(list(range(col)), weight=1)

    def setRows(self, row):
        self.grid_rowconfigure(list(range(row)), weight=1)

    def addFrame(self, row, col, rowspan=1, colspan=1):
        f = Frame(self, bg="blue")
        f.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew")

