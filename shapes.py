import numpy as np

class shape():
    def __init__(self, canvas):
        self.drawing = []
        self.canvas = canvas
    
    def erase(self):
        for idx in self.drawing:
            self.canvas.delete(idx)

# TODO: output is basically circuitikz code. Every element can be drawn separately. Try to figure out how to do this
class element(shape):
    shortcuts = {'r':'resistor',
                 'c':'capacitor',
                 'l':'inductor',
                 'V':'vsource',
                 'I':'isource',
                 'B':'depvsource',
                 'O':'depisource',
                 'w':'wire'}
    def __init__(self, canvas, start, end, shortcut):
        super().__init__(canvas)
        self.st = start
        self.ed = end
        self.t = shortcut

    def update_startpoint(self, start):
        self.st = start

    def update_endpoint(self,end):
        self.ed = end

    def copy(self):
        new_element = element(self.canvas, self.st, self.ed, self.t)
        return new_element

    def draw(self, color=None):
        self.erase()
        if color is None:
            color = 'blue' if self.t == 'w' else 'black'
        idx1 = self.canvas.create_line(*self.st, *self.ed, fill=color, width=3)
        center = (self.st + self.ed) / 2
        text_label = self.shortcuts[self.t]
        idx2 = self.canvas.create_text(*center, text=text_label, fill=color,font=('Helvetica 15'))
        self.drawing = [idx1, idx2]

class node(shape):
    shortcuts = {'g':'GND',
                 'a':'OPA',
                 'v':'NV'}

    def __init__(self, canvas, location, shortcut):
        super().__init__(canvas)
        self.loc = location
        self.t = shortcut

    def copy(self):
        new_node = node(self.canvas, self.loc, self.t)
        return new_node

    def update_location(self, location):
        self.loc = location

    def draw(self,color=None):
        self.erase()
        loc = self.loc
        ext1, ext2, ext3 = np.ones(2), np.array([-1, 1]), np.array([1, 0])
        text_label = self.shortcuts[self.t]
        if self.t == 'g' or self.t == 'v':
            color = 'blue' if color is None else color
            idx1 = self.canvas.create_line(*(loc+5*ext1), *(loc-5*ext1), fill=color, width=3)
            idx2 = self.canvas.create_line(*(loc+5*ext2), *(loc-5*ext2), fill=color, width=3)
            idx3 = self.canvas.create_text(*(loc+20*ext3), text=text_label,fill=color, font=('Helvetica 15'))
            self.drawing = [idx1, idx2, idx3]
        else:
            color = 'black' if color is None else color
            idx1 = self.canvas.create_line(*(loc+5*ext1), *(loc-5*ext1), fill=color, width=3)
            idx2 = self.canvas.create_line(*(loc+5*ext2), *(loc-5*ext2), fill=color, width=3)
            # TODO: WHY AM I DOING THIS. JUST DO A RECTANGLE THING
            idx3 = self.canvas.create_line(*loc, *(loc+20*(ext1+ext2)), fill=color, width=3)
            idx4 = self.canvas.create_line(*(loc+20*(ext1+ext2)), *(loc+40*ext1), fill=color, width=3)
            idx5 = self.canvas.create_line(*(loc+40*ext1), *(loc+20*(ext1-ext2)), fill=color, width=3)
            idx6 = self.canvas.create_line(*(loc+20*(ext1-ext2)), *loc, fill=color, width=3)
            idx7 = self.canvas.create_text(*(loc+20*ext1), text=text_label, fill=color, font=('Helvetica 15'))
            # TODO: make it look like an element at least
            self.drawing = [idx1, idx2, idx3, idx4, idx5, idx6, idx7] #TODO: also... can I not use eval? it seemed to be bugging out.

class handle(shape):
    def __init__(self, canvas, location, mode):
        super().__init__(canvas)
        self.loc = location
        self.m = mode
        self.draw()

    def update_info(self, location, mode):
        self.loc = location
        self.m = mode

    def copy(self):
        new_handle = handle(self.canvas, self.loc, self.m)
        return new_handle

    def draw(self, color='#000000'):
        self.erase()
        ext = np.ones(2)
        loc = self.loc
        idx1 = self.canvas.create_oval(*(loc - 3*ext), *(loc + 3*ext), fill=color)
        idx2 = self.canvas.create_oval(*(loc - 10*ext), *(loc + 10*ext), width=1, outline=color)
        idx3 = self.canvas.create_text(*(loc+ 10*ext), text=self.m, fill=color, font=('Helvetica 15'))
        self.drawing = [idx1, idx2, idx3]
