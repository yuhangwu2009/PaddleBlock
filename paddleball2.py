from tkinter import *
import random
import time

tk = Tk()
tk.title("Yuhang's First Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=1225, height=650, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

class Ball:
    def __init__(self, canvas, paddle, color, block_list):
        self.canvas = canvas
        self.paddle = paddle
        self.block_list = block_list
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 600, 300)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -1
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 1
        if not self.hit_paddle(pos):
            if not self.hit_block_bottom(pos):
                if not self.hit_block_top(pos):
                    self.hit_block_left(pos)
            
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.x = 1
        if pos[2] >= self.canvas_width:
            self.x = -1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.y = -1
                self.x += self.paddle.x
                return True
        return False

    def hit_block_bottom(self, pos):
        x = 0
        blocks = len(self.block_list)
        while x < blocks:
            if self.block_list[x].shown:
                block_pos = canvas.coords(self.block_list[x].id)
                if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
                    if pos[1] <= block_pos[3] and pos[3] >= block_pos[3]:
                        self.y = 1
                        block_list[x].hitted()
                        return True
            x += 1
        return False

    def hit_block_top(self, pos):
        x = 0
        blocks = len(self.block_list)
        while x < blocks:
            if self.block_list[x].shown:
                block_pos = canvas.coords(self.block_list[x].id)
                if pos[2] >= block_pos[0] and pos[0] <= block_pos[2]:
                    if pos[3] >= block_pos[1] and pos[1] <= block_pos[1]:
                        self.y = -1
                        block_list[x].hitted()
                        return True
            x += 1
        return False
    
    def hit_block_right(self, pos):
        x = 0
        blocks = len(self.block_list)
        while x < blocks:
            if self.block_list[x].shown:
                block_pos = canvas.coords(self.block_list[x].id)
                if pos[3] <= block_pos[1] and pos[1] >= block_pos[3]:
                    if pos[2] >= block_pos[0] and pos[0] <= block_pos[0]:
                        self.x = 1
                        block_list[x].hitted()
                        return True
            x += 1
        return False

    def hit_block_left(self, pos):
        x = 0
        blocks = len(self.block_list)
        while x < blocks:
            if self.block_list[x].shown:
                block_pos = canvas.coords(self.block_list[x].id)
                if pos[3] <= block_pos[1] and pos[1] >= block_pos[3]:
                    if pos[0] <= block_pos[2] and pos[2] >= block_pos[2]:
                        self.x = -1
                        block_list[x].hitted()
                        return True
            x += 1
        return False

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 1025, 530)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<Left>', self.turn_left)
        self.canvas.bind_all('<Right>', self.turn_right)
        self.canvas.bind_all('<Up>', self.speed_up)
        self.canvas.bind_all('<Down>', self.slow_down)
        self.canvas.bind("<Motion>",self.mouse_hand)
        self.canvas.bind_all('<Button-1>', self.start_game)
        self.speed = 1
        
    def mouse_hand(self, evt):  # runs on mouse motion
        pos = self.canvas.coords(self.id)
        width = pos[2] - pos[0]
        pos[0] = evt.x - width/2
        pos[2] = pos[0] + width
        self.x = 0
        self.canvas.coords(self.id, pos)
        self.canvas.config(cursor="none")

    def turn_left(self, evt):
        self.x = -speed

    def turn_right(self, evt):
        self.x = speed
        
    def speed_up(self, evt):
        self.speed += 1
        
    def slow_down(self, evt):
        self.speed -= 1
    
    def start_game(self, evt):
        self.started = True

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
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.x = x
        self.y = y
        self.color = color
        self.shown = True
        self.id = canvas.create_rectangle(x1, y1, width, height, fill=color)

    def hitted(self):
        canvas.delete(self.id)
        self.shown = False
        

paddle = Paddle(canvas, 'blue')
block1 = Block(canvas, 200, 100, 100, 50, 0, 0, 'brown')
block2 = Block(canvas, 400, 100, 300, 50, 3, 0, 'brown')
block3 = Block(canvas, 600, 100, 500, 50, 3, 0, 'brown')
block4 = Block(canvas, 800, 100, 700, 50, 3, 0, 'brown')
block5 = Block(canvas, 1000, 100, 900, 50, 3, 0, 'brown')
block6 = Block(canvas, 1200, 100, 1100, 50, 3, 0, 'brown')
block_list = [block1, block2, block3, block4, block5, block6]
ball = Ball(canvas, paddle, 'red', block_list)

while 1:
    if ball.hit_bottom == False and paddle.started:
        ball.draw()
        paddle.draw()
    if ball.hit_bottom == True:
        raise
    tk.update_idletasks()
    tk.update()
    time.sleep(0.003333333)
