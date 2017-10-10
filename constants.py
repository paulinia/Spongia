import pyglet
import os

FPS = 60
STEP = 1 / 50
size = 60
size_real = 100
N = 10
height = N * size_real
width = N * size_real

D = {pyglet.window.key.S : (0, -1),
     pyglet.window.key.W : (0, 1),
     pyglet.window.key.A : (-1, 0),
     pyglet.window.key.D : (1, 0)}

rotation = {(0, -1) : 180,
            (0, 1) : 0,
            (-1, 0) : 270,
            (1, 0) : 90}

pressed = {pyglet.window.key.W : False,
           pyglet.window.key.S : False,
           pyglet.window.key.A : False,
           pyglet.window.key.D : False,
           pyglet.window.key.ENTER : False}

