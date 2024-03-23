from tkinter import *
import numpy as np
from shapes import *
# import imutils

# functionality left over to do
# TODO: label (elements: labeled value, labeled voltage, labeled current, node voltage: values)
# TODO: rotate (only applies to ground) / anchor (only applies to node voltages) same behavior in principle, single thing. in increments of 45 degrees.
# TODO: print - if I want to save stuff whether as cktikz or editable circuits, It hink it would be nice to do a repr eval opposite thing / "isomoprhosim god dammint"

class Sketchpad(Canvas):
    special = {'m':'move',
               'd':'delete',
               'L':'label',
               'R':'rotate',
               'P':'print'}

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.current_element = None
        self.shape_to_highlight = None
        self.state = ' '
        self.shapes = {}

        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.release)
        self.bind("<Motion>", self.motion)
        self.bind("<KeyPress>", self.key_press)

    def key_press(self, event):
        key_input = event.char
        if key_input in self.special.keys():
            self.state = self.special[key_input]
        elif key_input in element.shortcuts.keys() or key_input in node.shortcuts.keys():
            self.state = key_input
        else:
            print(self.shapes)
            self.state = ' '

    def motion(self, event):
        cursor = self.get_cursor(event)
        cursor.draw()
        self.highlight_closest(self.grid_point(event))

    def grid_point(self, event):
        pt = np.array([event.x, event.y])
        snap = np.round(pt/20)*20
        return snap

    def get_cursor(self, event):
        snap = self.grid_point(event)

        exists = "cursor" in self.shapes.keys()
        cursor = None
        if exists:
            cursor = self.shapes["cursor"]
            cursor.update_info(snap, self.state)
        else:
            cursor = handle(self, snap, self.state)
            self.shapes["cursor"] = cursor
        return cursor

    def closest_editable_shape(self, pt, thresh=20):
        distance, closest, new_distance = np.infty, None, np.infty
        for name, shape in self.shapes.items():
            if isinstance(shape, node):
                new_distance = np.linalg.norm(pt - shape.loc)/2
            if isinstance(shape, element):
                displ = pt - shape.st
                seg = shape.ed - shape.st
                tangent_scale = np.sum(seg*displ)/np.sum(seg*seg)
                s = min(1, max(0, tangent_scale))
                new_distance = np.linalg.norm(displ - s * seg)
            if new_distance < distance:
                distance, closest = new_distance, (name, shape)
        if distance < thresh:
            return closest
        return None, None

    def highlight_closest(self, pt):
        _, new_shape = self.closest_editable_shape(pt)
        if self.shape_to_highlight is not new_shape:
            if self.shape_to_highlight is not None:
                self.shape_to_highlight.draw()
            self.shape_to_highlight = new_shape
            if new_shape is not None:
                new_shape.draw('green')

    def click(self, event):
        cursor = self.get_cursor(event)

        # Freeze the cursor where it was
        held_cursor = cursor.copy()
        held_cursor.draw("red")
        self.shapes["held_cursor"] = held_cursor

        # Freeze a possibly active shape where it was
        if self.shape_to_highlight is not None:
            held_shape = self.shape_to_highlight.copy()
            held_shape.draw("red")
            self.shapes["held_shape"] = held_shape

        self.delete_closest_shape(event)

    def delete_closest_shape(self, event):
        if self.state == 'delete':
            pt = self.grid_point(event)
            name_to_delete, shape_to_delete  = self.closest_editable_shape(pt)
            if name_to_delete is not None:
                self.delete_shape(name_to_delete)
            if self.shape_to_highlight is shape_to_delete:
                self.shape_to_highlight = None

    def drag(self, event):
        cursor = self.get_cursor(event)
        cursor.draw()
        self.add_element(event)
        self.move_closest_shape(event)

    def move_closest_shape(self, event):
        inrange_shape = self.shape_to_highlight
        if self.state == 'move' and inrange_shape is not None:
            pt = self.grid_point(event)
            held_shape = self.shapes['held_shape']
            prev_loc = self.shapes['held_cursor'].loc
            if isinstance(inrange_shape, node):
                inrange_shape.update_location(pt)
                inrange_shape.draw('green')
            if isinstance(self.shape_to_highlight, element):
                if np.linalg.norm(prev_loc - held_shape.ed) > 10:
                    inrange_shape.update_startpoint(held_shape.st + pt - prev_loc)
                if np.linalg.norm(prev_loc - held_shape.st) > 10:
                    inrange_shape.update_endpoint(held_shape.ed + pt - prev_loc)
                inrange_shape.draw('green')
        
    def release(self, event):
        self.delete_shape('held_cursor')
        self.delete_shape('held_shape')
        snap = self.grid_point(event)
        self.add_node(snap)
        self.current_element = None

    def delete_shape(self, shape_name):
        if shape_name in self.shapes.keys():
            self.shapes[shape_name].erase()
            self.shapes.pop(shape_name)

    def add_node(self, pt):
        if self.state in node.shortcuts.keys():
            shape_name = node.shortcuts[self.state]
            idx = 0
            idxed_name = shape_name + str(idx)
            while idxed_name in self.shapes.keys():
                idx += 1
                idxed_name = shape_name + str(idx)
            new_shape = node(self, pt, self.state)
            self.shapes[idxed_name] = new_shape
            new_shape.draw()

    def add_element(self,event):
        pt = self.grid_point(event)
        if self.current_element is None:
            if self.state in element.shortcuts.keys():
                shape_name = element.shortcuts[self.state]
                idx = 0
                idxed_name = shape_name + str(idx)
                while idxed_name in self.shapes.keys():
                    idx += 1
                    idxed_name = shape_name + str(idx)
                start_pt = self.shapes['held_cursor'].loc
                new_shape = element(self,start_pt,pt, self.state)
                self.shapes[idxed_name] = new_shape
                new_shape.draw()
                self.current_element = new_shape
        else:
            self.current_element.update_endpoint(pt)
            self.current_element.draw()