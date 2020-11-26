from tkinter import *
import random
import time

tk = Tk()
tk.title("Yuhang's First Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

class Ball:
    def __init__(self, canvas, paddle, color, block_list):
        self.canvas = canvas
        self.paddle = paddle
        self.block_list = block_list
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        self.hit_paddle(pos)
        if self.hit_paddle(pos) == False:
            hit_block_bottom(pos, block_list)
            hit_block_top(pos, block_list)
            
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.y = -3
                return True
        return False

    def hit_block_bottom(self, pos, block_list):
        x = 0
        blocks = len(block_list)
        while x < blocks:
            block_pos = canvas.coords(self.block_list(x).id)
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
                if pos[1] <= block_pos[3] and pos[1] >= block_pos[1]:
                    self.y = -3
                    return True
                    break
            x += 1

    def hit_block_top(self, pos, block_list):
        x = 0
        blocks = len(block_list)
        while x < blocks:
            block_pos = canvas.coords(self.block_list(x).id)
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
                if pos[1] >= block_pos[3] and pos[1] <= block_pos[1]:
                    self.y = 3
                    return True
                    break
            x += 1

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<Left>', self.turn_left)
        self.canvas.bind_all('<Right>', self.turn_right)
        self.canvas.bind("<Motion>",self.mouse_hand)
        
    def mouse_hand(self, evt):  # runs on mouse motion
        pos = self.canvas.coords(self.id)
        width = pos[2] - pos[0]
        pos[0] = evt.x - width/2
        pos[2] = pos[0] + width
        self.x = 0
        self.canvas.coords(self.id, pos)
        self.canvas.config(cursor="none")

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

class Block:
    def __init__(self, canvas, x1, y1, width, height, x, y, color):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.id = canvas.create_rectangle(x1, y1, width, height, fill=color)
    def disappear(self):
        canvas.delete(self.id)
        

paddle = Paddle(canvas, 'blue')
block1 = Block(canvas, 30, 30, 460, 50, 0, 0, 'brown')
block_list = [block1]
ball = Ball(canvas, paddle, 'red', block_list)

while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
