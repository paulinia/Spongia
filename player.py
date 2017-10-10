from constants import *
from utility import *

class Player:
    def __init__(self, x, y, batch):
        self.x = x
        self.y = y
        self.clothing = "Leather"
        self.imag = pyglet.resource.image(os.path.join("graphics", self.clothing + ".png"))
        self.imag.anchor_x, self.imag.anchor_y = self.imag.width // 2, self.imag.height // 2
        self.sprite = pyglet.sprite.Sprite(self.imag, compute_position(self.x, self.y)[0], compute_position(self.x, self.y)[1], batch=batch)
        self.sprite.scale = (size_real / size)
    
    def step(self, di, level):
        dx, dy = di
        self.sprite.rotation = rotation[di]
        can = level.can_move((self.x + dx, self.y + dy), di)
        if can[0]:
            self.x = dx + self.x
            self.y = dy + self.y
            nx, ny  = compute_position(self.x, self.y)
            self.sprite.set_position(nx, ny)
            if can[1] != "":
                self.clothing = can[1]
                self.imag = pyglet.resource.image(os.path.join("graphics", self.clothing + ".png"))
                self.imag.anchor_x, self.imag.anchor_y = self.imag.width // 2, self.imag.height // 2
                self.sprite = pyglet.sprite.Sprite(self.imag, compute_position(self.x, self.y)[0], compute_position(self.x, self.y)[1], batch=can[2])
                self.sprite.scale = (size_real / size)
                self.sprite.rotation = rotation[di]
    
    def explode(self, batch):
        self.imag = pyglet.resource.image(os.path.join("graphics", "Dead1.png"))
        self.imag.anchor_x, self.imag.anchor_y = self.imag.width // 2, self.imag.height // 2
        self.sprite = pyglet.sprite.Sprite(self.imag, compute_position(self.x, self.y)[0], compute_position(self.x, self.y)[1], batch=batch)
        self.sprite.scale = (size_real / size)
        return (self.x, self.y)
