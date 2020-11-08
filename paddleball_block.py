from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
    
    def hit_block(self, blocks):
        for i in blocks:
            List = [self.pos]
            for i in List:
                if pos[0] >= i[0] and pos[2] <= i[2]:
                    if pos[1] >= i[1] and pos[1] <= i[3]:
                        canvas.delete(self.id)
                        self.score()
                        global a
                        a += 1
                        return True

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<space>', self.start_game)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def start_game(self, evt):
        self.started = True

class Block:
    def __init__(self, canvas, color, x1, y1, x2, y2):
        self.canvas = canvas
        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.id = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color)
        self.pos = [x1, y1, x2, y2]
        self.x = 0
    
    def hit_block(self, pos):
        List = [self.pos]
        for i in List:
            if pos[0] >= i[0] and pos[2] <= i[2]:
                if pos[1] >= i[1] and pos[1] <= i[3]:
                    canvas.delete(self.id)
                    self.score()
                    global a
                    a += 1
                    return True
        return False
    
    def draw(self):
        canvas.move(self.id, self.x, 0)
        

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, fill=color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

score = Score(canvas, 'green')
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, score, 'red')
block1 = Block(canvas,'brown', 10, 10, 50, 300)
blocklist = [block1]
while 1:
    if ball.hit_bottom == False and paddle.started == True:
        ball.draw()
        paddle.draw()
        block1.hit_block(canvas.coords(ball))
        ball.hit_block(blocklist)
    if ball.hit_bottom == True:
        time.sleep(1)
        canvas.create_text(250, 200, text='GAME OVER', state = 'normal', font=('Courier'))

    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
