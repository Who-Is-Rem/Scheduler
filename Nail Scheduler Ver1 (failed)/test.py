from tkinter import Tk, Label, Frame, Canvas, Scrollbar, PhotoImage

def yview(action, fraction):
    canvas.yview(action, fraction)
    x, y = canvas.coords(bg)
    dy = canvas.canvasy(0)-y
    canvas.move(bg, 0, dy)

image_file = "/Users/al/Documents/csProjects/Nail Scheduler (py)/images/xMark.png"

root = Tk()

vscrollbar = Scrollbar(root, orient='vertical')
vscrollbar.pack(side='right', fill='y', expand=0)

canvas = Canvas(root, width=800, height=800, bg='green', yscrollcommand=vscrollbar.set)
canvas.pack(side='left', padx=0, pady=0, ipadx=0, ipady=0)

vscrollbar.configure(command=yview)

image = PhotoImage(file=image_file)
bg = canvas.create_image(0, 0, image=image, anchor='nw')

# ========================  Block  ======================================
frame = Frame(canvas)
frame_id = canvas.create_window(800//2, 0, window=frame, anchor="n")

for i in range(30):
    Label(frame, text=f'Label {i+1:0>2d}', padx=5, pady=5).pack()
# ==================================================================

canvas.update()
canvas.configure(scrollregion=canvas.bbox('all'))

root.mainloop()

