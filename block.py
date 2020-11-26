import tkinter as tk

class BaseObj(object):
    def __init__(self, canvas, obj):
        self.canvas = canvas
        self.obj = obj

    def get_position(self):
        return self.canvas.coords(self.obj)

    def move(self, x, y):
        self.canvas.move(self.obj, x, y)

    def delete(self):
        self.canvas.delete(self.obj)
