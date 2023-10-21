# Scheduler
Scheduling GUI that will be specialized towards a Nail Salon Business. Hopefully, it will be developed 
so some classes can be used in other projects.

This scheduler will use tkinter, pydrive2, pickle, time, etc. from Python. The goal of this is to make 
a functional scheduler with draggable widgets that can be edited, deleted, and--of course--moved. There 
will be a separate folder containing the code of failed past iterations that I will keep for reference 
and just to see how badly I failed in the past. These past iterations are mainly from me playing around 
with the tkinter package and seeing what I can, some of the functionalities exist, and some do not, 
depending on the iteration. 

Before making this repository, I already had 3 failed iterations of the scheduler. Some of the issues I 
have faced so far include but are not limited to extensive widget ancestry, bad template for widgets, 
threads overlapping in functionality, pickle files getting deleted, and a never-ending while loop. 

Some goals I should cover as I make the scheduler: have a template for widget placement, decrease widget 
count from creating a spreadsheet, partition core components of the scheduler and test them separately, 
smooth dnd of draggable widgets, connection to Google Drive and uploading and loading of files, saving 
information with pickle files or some other method, a queue for customer frames, and, if I can, a pop up 
frame containing more detailed information pertaining to a customer as fitting a lot of information into 
a tiny frame looks ugly. Ah, and of course, further research tkinter's functionality as I barely touched 
the tip of the iceberg, search for prebuilt, efficient spreadsheets that fit this project, and if 
nonexistent try to utilize Tk.separators with grid layout instead of a bunch of labels with borders. 
