from canvas import *

root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root, bg="white", cursor="circle")
sketch.grid(column=0, row=0, sticky=(N, W, E, S))
sketch.focus_set()
sketch.config(cursor="none")

grid_spacing = 10

# drawing gridlines
for i in range(1280//grid_spacing):
    grid_color = '#f0f0f0' if i % 2 else '#d0d0d0'
    width = 1 #if i % 2 else 1
    sketch.create_line((grid_spacing*(i+1), 0, grid_spacing*(i+1), 720), width=width, fill=grid_color)
for i in range(720//grid_spacing):
    grid_color = '#f0f0f0' if i % 2 else '#d0d0d0'
    width = 1 #if i % 2 else 1
    sketch.create_line((0, grid_spacing*(i+1), 1280, grid_spacing*(i+1)), width=width, fill=grid_color)

# On replacing mainloop:
# https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
root.mainloop()
