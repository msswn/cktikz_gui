import numpy as np

class shape():
    def __init__(self, canvas):
        self.drawing = []
        self.canvas = canvas

    # this is needed because of canvas coordinates vs. latex coordinates
    transform = lambda self, x: np.array([[1, 0], [0, -1]])@x # invert coords..

    def erase(self):
        for idx in self.drawing:
            self.canvas.delete(idx)

class element(shape):
    shortcuts = {'r':'resistor',
                 'c':'capacitor',
                 'l':'inductor',
                 'V':'vsource',
                 'I':'isource',
                 'B':'depvsource',
                 'O':'depisource',
                 'w':'wire',
                 'o':'open',
                 'd':'diode'}
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

    latex_str = {'r':'R',
                 'c':'C',
                 'l':'L',
                 'V':'V',
                 'I':'I',
                 'B':'cV',
                 'O':'cI',
                 'w':'short',
                 'o':'open',
                 'd':'diode'}
    label_str = {'r':'l=$\\si{\\ohm}$',
                 'c':'l=$\\si{\\farad}$',
                 'l':'l=$\\si{\\henry}$',
                 'V':'l=$\\si{\\volt}$',
                 'I':'l=$\\si{\\ampere}$',
                 'B':'',
                 'O':'',
                 'w':'',
                 'o':'v=$$',
                 'd':''}
    def str_latex(self,label_info):
        start_coord = tuple([float(a) for a in self.transform(self.st/40)])
        end_coord = tuple([float(a) for a in self.transform(self.ed/40)])
        label_str = self.label_str[self.t]
        cktikz_str = self.latex_str[self.t]
        return f'\\draw{start_coord} to[{cktikz_str},{label_str}] {end_coord};'

# to add a new node:
# update shortcuts
# update drawing
# update latex_str list
# update str_latex function

class node(shape):
    shortcuts = {'g':'GND',
                 'a':'OPA',
                 'v':'NV',
                 'n':'NPN',
                 'p':'PNP',
                 'N':'PMOS',
                 'P':'NMOS'}

    def __init__(self, canvas, location, shortcut):
        super().__init__(canvas)
        self.loc = location
        self.t = shortcut
        self.angle = 0

    def copy(self):
        new_node = node(self.canvas, self.loc, self.t)
        new_node.angle = self.angle
        return new_node

    def update_location(self, location):
        self.loc = location

    # TODO: finish this
    def flip(self,along):
        # along is a character, either 'X' or 'Y'
        pass

    def rotate(self):
        if self.t != 'a':
            self.angle = (self.angle + 1) % 8 
            self.draw()

    def rot45(self, angle):
        c, s = np.cos(np.pi/4*angle), np.sin(np.pi/4*angle)
        return np.array([[c,-s],[s,c]])

    def draw_x(self, loc, color):
        ext1, ext2 = np.ones(2), np.array([-1, 1])
        idx1 = self.canvas.create_line(*(loc+5*ext1), *(loc-5*ext1), fill=color, width=3)
        idx2 = self.canvas.create_line(*(loc+5*ext2), *(loc-5*ext2), fill=color, width=3)
        return [idx1, idx2]

    def draw(self,color=None):
        self.erase()
        loc = self.loc
        ext1, ext2, ext3, ext4 = np.ones(2), np.array([-1, 1]), np.array([1, 0]), np.array([0, 1])
        text_label = self.shortcuts[self.t]
        if self.t in ['g','v']:
            color = 'blue' if color is None else color
            M = self.rot45(self.angle)
            ext1, ext2, ext3, ext4 = M @ ext1, M @ ext2, M @ ext3, M @ ext4
            off = loc+10*ext4
            idx1 = self.canvas.create_line(*loc, *off, fill=color, width=3)
            idx2, idx3 = self.draw_x(off,color)
            idx4 = self.canvas.create_text(*(off+20*ext4), text=text_label,fill=color, font=('Helvetica 15'))
            self.drawing = [idx1, idx2, idx3, idx4]
        if self.t == 'a':
            color = 'black' if color is None else color
            idx1, idx2 = self.draw_x(loc, color)
            shift = np.array([0.625,0.25])
            idx3 = self.canvas.create_rectangle(*(loc-40*shift+40*0.625*ext3), *(loc+40*shift+40*0.625*ext3), outline=color, width=3)
            idx4 = self.canvas.create_text(*(loc+20*ext1), text=text_label, fill=color, font=('Helvetica 15'))
            # TODO: make it look like an element at least. Add the nodes for the op amp
            self.drawing = [idx1, idx2, idx3, idx4] #TODO: also... can I not use eval? it seemed to be bugging out.
        if self.t in ['n','p','N','P']:
            M = self.rot45(self.angle)
            ext1, ext2, ext3, ext4 = M @ ext1, M @ ext2, M @ ext3, M @ ext4
            color = 'black' if color is None else color
            idx1, idx2 = self.draw_x(loc, color)
            shift = np.array([0.5, 0.5]) * 40
            idx3 = self.canvas.create_line(*(loc+20*ext1), *(loc-20*ext2),fill=color, width=3)
            idx4 = self.canvas.create_line(*(loc+20*ext3), *(loc-20*ext3),fill=color, width=3)
            idx5 = self.canvas.create_text(*(loc+20*ext1), text=text_label, fill=color, font=('Helvetica 15'))
            self.drawing = [idx1, idx2, idx3, idx4, idx5]

    latex_str = {'g':'ground',
                 'a':'op amp',
                 'v':'',
                 'n':'npn',
                 'p':'pnp',
                 'N':'nmos',
                 'P':'pmos,emptycircle'}

    anchor_str = ['north', 'north east', 'east','south east' , 'south', 'south west', 'west']

    def str_latex(self, label_info):
        coord = tuple([float(a) for a in self.transform(self.loc/40)])
        cktikz_str = self.latex_str[self.t]
        label_str = ''
        extra_str = ''

        # ground
        if self.t == 'g':
            cktikz_str += f',rotate={-self.angle * 45}'

        # node voltage label
        if self.t == 'v':
            cktikz_str += f'anchor={self.anchor_str[self.angle]}'
            label_str = '$V$'

        # Normal op amp coordinates are:
        # If you place op amp at (0, 0)
        # output at (1.19, 0)
        # terminals at: (-1.19, +/-0.49)
        # I'm assuming with a scaledown factor of 0.51
        # output: (0.61, 0)
        # terminals: (-0.61, +/-0.25)

        # amplifier: drawn for a scale down factor of 0.51 in cktikz
        if self.t == 'a':
            loc = self.transform(self.loc/40)+np.array([0.61, 0])
            coord = tuple([float(a) for a in np.round(loc,2)])
            to_edge = np.array([0.03, 0])
            out = loc + np.array([0.61,0])
            amp_wire_start_loc = tuple([float(a) for a in np.round(out, 2)])
            amp_wire_end_loc = tuple([float(a) for a in np.round(out+to_edge,2)])
            extra_str+= f'{amp_wire_start_loc} to[short] {amp_wire_end_loc}'

        # transistors: drawn for a scale down factor of 0.65 in cktikz
        if self.t in ['n','p','N','P']:
            cktikz_str += f',rotate={-self.angle * 45}'
            M = self.rot45(-self.angle)
            loc = self.transform(self.loc/40) + M@np.array([0.5,0])
            coord = tuple([float(a) for a in loc])
            # default BJT
            control = loc + M@np.array([-0.55,0])
            to_edge = M@np.array([0.45, 0])
            if self.t.isupper():
                # MOSFET
                delta = M@np.array([-0.09, 0])
                control += delta;
                to_edge += delta;
            extra_str = f'{tuple([float(a) for a in control])} to[short] {tuple([float(a) for a in control-to_edge])}';

        return f'\\draw{coord} node[{cktikz_str}]{{{label_str}}}{extra_str};'

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
