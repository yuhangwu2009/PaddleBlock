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

def hit_block():
    pos = canvas.coords(ball.id)
    block_pos = canvas.coords(block1.id)

    if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
        if pos[1] <= block_pos[3] and pos[1] >= block_pos[1]:
            return True

def hit_block_top():
    pos = canvas.coords(ball.id)
    block_pos = canvas.coords(block1.id)
    if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
        if pos[3] >= block_pos[1] and pos[3] <= block_pos[3]:
            return True

class Ball:
    def __init__(self, canvas, paddle, block, color):
        self.canvas = canvas
        self.paddle = paddle
        self.block = block
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 200)
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
        if self.hit_paddle(pos) == True:
            self.y = -3
        if self.hit_block == True:
            self.y = -3
        if self.hit_block_top == True:
            self.y = 3
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
                return True
        return False
    def hit_block(self):
        pos = canvas.coords(self.id)
        block_pos = canvas.coords(block.id)
        if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
            if pos[1] <= block_pos[3] and pos[1] >= block_pos[1]:
                return True
            
    def hit_block_top(self):
        pos = canvas.coords(self.id)
        block_pos = canvas.coords(block.id)
        if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
            if pos[3] >= block_pos[1] and pos[3] <= block_pos[3]:
                return True

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<Left>', self.turn_left)
        self.canvas.bind_all('<Right>', self.turn_right)
        self.canvas.bind_all('<Up>', self.speed_up)
        self.canvas.bind_all('<Down>', self.speed_down)
        self.canvas.bind("<Motion>",self.mouse_hand)
        self.speed = 2

    def mouse_hand(self, evt):  # runs on mouse motion
        pos = self.canvas.coords(self.id)
        width = pos[2] - pos[0]
        pos[0] = evt.x - width/2
        pos[2] = pos[0] + width
        self.x = 0
        self.canvas.coords(self.id, pos)
        self.canvas.config(cursor="none")

    def speed_up(self, evt):
        self.speed += 1
    def speed_down(self,evt):
        self.speed -= 1
    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

class Block:
    def __init__(self, canvas, color, x1, y1, x2, y2):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, x2, y2, fill=color)
        self.canvas.move(self.id, x1, y1)
    if hit_block == True:
        self.canvas.delete(self.id)
    elif hit_block_top == True:
        self.canvas.delete(self.id)
    
    def hit_block_top(self):
        pos = canvas.coords(self.ball.id)
        block_pos = canvas.coords(self.id)
        if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
            if pos[3] >= block_pos[1] and pos[3] <= block_pos[3]:
                return True
            
    def hit_block(self):
        pos = canvas.coords(self.ball.id)
        block_pos = canvas.coords(self.id)
        if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
            if pos[1] <= block_pos[3] and pos[1] >= block_pos[1]:
                return True
        
paddle = Paddle(canvas, 'blue')
block1 = Block(canvas, 'green', 230, 100, 100, 20)
ball = Ball(canvas, paddle, block1, 'red')
block_list = [block1]

while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
