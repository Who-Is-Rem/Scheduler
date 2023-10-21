from tkinter import *

# Approxiamte center cords of the screen
centerX = 720
centerY = 420


# Creation of window and initialization
root = Tk()
root.title("Cara Nails Scheduler")
root.minsize(750,500)
root.geometry("750x500+345+170")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Creation of main containers
top_frame = Frame(root, bg='red', width=root.winfo_screenwidth(), height=60, pady=3, padx=3)
center = Canvas(root, bg='gray', width=root.winfo_screenwidth()-20, height=root.winfo_screenheight()-60)
scrollbar = Scrollbar(root, width = 20)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="news")
scrollbar.grid(row=1, sticky="nse")

# Initialization of the top frame
# Paths for the pictures of the arrows used for previous and next buttons
leftPhoto = PhotoImage(file="")
rightPhoto = PhotoImage(file="")

# Creation of the button on the top frame
employeeButton = Button(top_frame, text="Employees", padx = 1, pady = 1, bg="gray")
resetButton = Button(top_frame, text = "Reset", bg="gray", padx = 1, pady = 1)
customerButton = Button(top_frame, text="Customer", padx = 1, pady = 1, bg="gray")
# Needs to be adjusted to add the pictures to the buttons, may end up using sprites 
previousButton = Button(top_frame, image = "", bg="gray")
changeDate = Button(top_frame, text = "Change Date", bg="gray", padx = 1, pady = 1)
nextButton = Button(top_frame, image = "", bg="gray")

top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=0)
top_frame.grid_rowconfigure(1, weight=1)

employeeButton.grid(row=0, column=0, sticky="w", pady=2)
customerButton.grid(row=0, column=2, sticky = "e", pady=2)
resetButton.grid(row=0, column=1, pady=2)

previousButton.grid(row=1, column=0, sticky="w", pady=2)
changeDate.grid(row=1, column=1, pady=2)
nextButton.grid(row=1, column=2, sticky="e", pady=2)

# Initialization of the central scheduler that function with the scroll bar
root.mainloop()