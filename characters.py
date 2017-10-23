from constants import *
from utility import *
import random

class Person:
    def __init__(self, name, x, y, batch, score, direct):
        self.x = x
        self.y = y
        self.direction = 0
        self.name = name
        self.imag = pyglet.resource.image(os.path.join("graphics", name + ".png"))
        self.imag.anchor_x, self.imag.anchor_y = self.imag.width // 2, self.imag.height // 2
        self.sprite = pyglet.sprite.Sprite(self.imag, compute_position(self.x, self.y)[0], compute_position(self.x, self.y)[1], batch=batch)
        self.sprite.scale = (size_real / size)
        translate = {"W" : (0, 1),
                     "S" : (0, -1),
                     "A" : (-1, 0),
                     "D" : (1, 0)}
        self.movement = [translate[c] for c in direct]
        self.score = int(score)
        self.stopped = 0
        self.turned = 0
        
    def move(self, level):
        if self.stopped != 0:
            self.stopped -= 1
            return None
        if self.turned != 0:
            self.turned -= 1
            res = level.blocked((self.x + self.movement[self.direction][1], self.y + self.movement[self.direction][0]))
            if not res[0]:
                if res[1] == "stop":
                    self.stopped += 2
                    return None
                if res[1] == "turn":
                    self.turned = 2
                    return None
            else:
                self.x += self.movement[self.direction][1]
                self.y += self.movement[self.direction][0]
                x, y = compute_position(self.x, self.y)
                self.sprite.set_position(x, y)
            self.sprite.rotation = rotation[(self.movement[self.direction][1], self.movement[self.direction][0])]
            return None
        res = level.blocked((self.x + self.movement[self.direction][0], self.y + self.movement[self.direction][1]))
        if not res[0]:
            if res[1] == None:
                self.direction = (1 + self.direction) % len(self.movement)
            if res[1] == "stop":
                self.stopped += 2
                self.direction = (1 + self.direction) % len(self.movement)
                #return None
            if res[1] == "turn":
                self.turned = 2
                #return None
        else:
            self.x += self.movement[self.direction][0]
            self.y += self.movement[self.direction][1]
            x, y = compute_position(self.x, self.y)
            self.sprite.set_position(x, y)
        self.sprite.rotation = rotation[self.movement[self.direction]]
        
    def die(self, batch):
        self.imag = pyglet.resource.image(os.path.join("graphics", self.name + "Dead.png"))
        self.imag.anchor_x, self.imag.anchor_y = self.imag.width // 2, self.imag.height // 2
        self.sprite = pyglet.sprite.Sprite(self.imag, compute_position(self.x, self.y)[0], compute_position(self.x, self.y)[1], batch=batch)
        self.sprite.scale = (size_real / size)
        return self.score
