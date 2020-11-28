import tkinter as tk


class BaseObj(object):
    def __init__(self, canvas, id):
        self.canvas = canvas
        self.id = id

    def get_position(self):
        return self.canvas.coords(self.id)

    def move(self, x, y):
        self.canvas.move(self.id, x, y)

    def delete(self):
        self.canvas.delete(self.id)


class Paddle(BaseObj):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = self.width/8
        self.ball = None
        self.started = False
        id = canvas.create_rectangle(x - self.width / 2,
                                     y - self.height / 2,
                                     x + self.width / 2,
                                     y + self.height / 2,
                                     fill='yellow')
        super(Paddle, self).__init__(canvas, id)

    def set_ball(self, ball):
        self.ball = ball
        self.started = False

    def move(self, x):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        offset = x - coords[0] - self.width / 2
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if not self.started:
                self.ball.move(offset, 0)

    def hit(self, ball):
        ballcoords = ball.get_position()
        coords = self.get_position()
        ballx = (ballcoords[0] + ballcoords[2]) * 0.5
        x = (coords[0] + coords[2]) * 0.5
        self.ball.speedx *= (1 + (ballx - x) / self.width)


class Ball(BaseObj):
    def __init__(self, canvas, x, y):
        self.radius = 6
        self.direction = [1, -1]
        self.speedx = 10
        self.speedy = 10
        self.rate = 1
        id = canvas.create_oval(x - self.radius, y - self.radius,
                                x + self.radius, y + self.radius,
                                fill='white')
        super(Ball, self).__init__(canvas, id)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speedx * self.rate
        y = self.direction[1] * self.speedy * self.rate
        self.move(x, y)

    def collide(self, objs):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(objs) > 1:
            self.direction[1] *= -1
        elif len(objs) == 1:
            obj = objs[0]
            coords = obj.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        for obj in objs:
            obj.hit(self)


class Block(BaseObj):
    COLORS = {1: '#e74c3c', 2: '#3498db', 3: '#222222'}

    def __init__(self, canvas, x, y, hits = 1):
        self.width = 40
        self.height = self.width/2
        self.hits = hits
        color = Block.COLORS[hits]
        id = canvas.create_rectangle(x - self.width / 2,
                                     y - self.height / 2,
                                     x + self.width / 2,
                                     y + self.height / 2,
                                     fill=color, tags='Block')
        super(Block, self).__init__(canvas, id)

    def hit(self, ball = None):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.id,
                                   fill=Block.COLORS[self.hits])

class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.availible_balls = 3
        self.level = 1
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#aaaaff',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()
        self.pack()

        self.objs = {}
        self.balls = {}
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.objs[self.paddle.id] = self.paddle
        self.level_depl(self.level)

        self.info = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind("<Motion>", self.mouse_hand)

    def mouse_hand(self, evt):  # runs on mouse motion
        self.paddle.move(evt.x)

    def setup_game(self):
           self.add_ball()
           self.update_lives_text()
           self.text = self.draw_text(300, 200,
                                      'Click to start')
           self.canvas.bind('<Button-1>', lambda _: self.start_game())

    def add_ball(self):
        for id, ball in self.balls.items():
            ball.delete()
        if len(self.balls) > 0:
            self.balls.clear()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        ball = Ball(self.canvas, x, 314)
        self.balls[ball.id] = ball
        self.paddle.set_ball(ball)

    def level_depl(self, level):
        if level == 2:
            for x in range(5, self.width - 5, 75):
                self.add_block(x + 37.5, 50, 2)
                self.add_block(x + 37.5, 80, 1)
                self.add_block(x + 37.5, 110, 1)

        if level == 3:
            for x in range(5, self.width - 5, 75):
                self.add_block(x + 37.5, 50, 3)
                self.add_block(x + 37.5, 70, 2)
                self.add_block(x + 37.5, 90, 1)

        if level == 4:
            for x in range(5, self.width - 5, 75):
                self.add_block(x + 37.5, 50, 3)
                self.add_block(x + 37.5, 70, 3)
                self.add_block(x + 37.5, 90, 3)

        if level == 1:
            for x in range(5, self.width-75, 40):
                self.add_block(x + 37.5, 50, 1)
                self.add_block(x + 37.5, 70, 1)
                self.add_block(x + 37.5, 90, 1)
                self.add_block(x + 37.5, 110, 1)
                self.add_block(x + 37.5, 130, 1)
                self.add_block(x + 37.5, 150, 1)
    def add_block(self, x, y, hits):
        block = Block(self.canvas, x, y, hits)
        self.objs[block.id] = block

    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_lives_text(self):
        text = 'Level: %s | Extra Balls: %s' %(self.level, self.availible_balls)
        if self.info is None:
            self.info = self.draw_text(120, 20, text, 15)
        else:
            self.canvas.itemconfig(self.info, text=text)

    def start_game(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.delete(self.text)
        self.paddle.started = True
        self.game_loop()

    def reset_ballsspeed(self):
        for id, ball in self.balls.items():
            ball.rate = None

    def check_activeballs(self):
        deadballs = {id: ball for id, ball in self.balls.items()
                      if ball.get_position()[3] >= self.height}
        for id in deadballs.keys():
            self.balls.pop(id)
            deadballs[id].delete()
        return len(self.balls)

    def update_balls(self):
        for id, ball in self.balls.items():
            ball.update()

    def game_loop(self):
        self.check_collisions()
        num_Blocks = len(self.canvas.find_withtag('Block'))
        if num_Blocks == 0:
            self.level += 1
            self.level_depl(self.level)
            self.setup_game()
            self.start_game()
            self.availible_balls += self.level
        elif self.check_activeballs() == 0:
            self.availible_balls -= 1
            if self.availible_balls < 0:
                self.draw_text(300, 200, 'You Lose! Game Over!')
            else:
                self.after(1000, self.setup_game)
        else:
            self.update_balls()
            self.after(50, self.game_loop)

    def check_collisions(self):
        for id, ball in self.balls.items():
            ball_coords = ball.get_position()
            objs = self.canvas.find_overlapping(*ball_coords)
            objects = [self.objs[x] for x in objs if x in self.objs]
            ball.collide(objects)



if __name__ == '__main__':
    root = tk.Tk()
    root.title('Ball Game')
    game = Game(root)
    game.mainloop()