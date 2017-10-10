from constants import *
import random

class Person:
    def __init__(self, name, x, y, batch):
        self.x = x
        self.y = y
        self.direction = random.randint(0, 3)
        self.name = name
        self.imag = pyglet.resource.image(os.path.join("graphics", name + ".png"))
        self.imag.anchor_x, self.imag.anchor_y = self.imag.width // 2, self.imag.height // 2
        self.sprite = pyglet.sprite.Sprite(self.imag, compute_position(self.x, self.y)[0], compute_position(self.x, self.y)[1], batch=batch)
        self.sprite.scale = (size_real / size)
        
    def move(self, level):
        while not level.blocked((self.x + DR[self.direction][0], self.y + DR[self.direction][1])):
            self.direction = random.randint(0, 3)
            self.sprite.rotation = rotation[DR[self.direction]]
        self.x += DR[self.direction][0]
        self.y += DR[self.direction][1]
        self.sprite.set_position(self.x, self.y)
