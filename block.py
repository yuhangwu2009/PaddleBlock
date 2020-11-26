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

class Paddle(BaseObj):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        self.started = False
        obj = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='yellow')
        super(Paddle, self).__init__(canvas, obj)

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

    def hit(self):
        ballcoords = self.ball.get_position()
        coords = self.get_position()
        ballx = (ballcoords[0] + ballcoords[2]) * 0.5
        x = (coords[0] + coords[2]) * 0.5
        self.ball.speedx *= (1+(ballx - x)/self.width)

class Ball(BaseObj):
    def __init__(self, canvas, x, y):
        self.radius = 8
        self.direction = [1, -1]
        self.speedx = 10
        self.speedy = 10
        obj = canvas.create_oval(x-self.radius, y-self.radius,
                                 x+self.radius, y+self.radius,
                                 fill='white')
        super(Ball, self).__init__(canvas, obj)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speedx
        y = self.direction[1] * self.speedy
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
            obj.hit()
