import pyglet
import os

FPS = 60
STEP = 1 / 50
size = 60
size_real = 80
N = 12
height = N * size_real
width = N * size_real

D = {pyglet.window.key.S : (0, -1),
     pyglet.window.key.W : (0, 1),
     pyglet.window.key.A : (-1, 0),
     pyglet.window.key.D : (1, 0)}

DR = [(0, -1), (0, 1), (-1, 0), (1, 0)]

rotation = {(0, -1) : 180,
            (0, 1) : 0,
            (-1, 0) : 270,
            (1, 0) : 90}

pressed = {pyglet.window.key.W : False,
           pyglet.window.key.S : False,
           pyglet.window.key.A : False,
           pyglet.window.key.D : False,
           pyglet.window.key.ENTER : False}

explosion = pyglet.resource.media(os.path.join('audio', 'Explosion.wav'), streaming = False)
audio_levels = {"MENU":    pyglet.resource.media(os.path.join("audio", "Battle Lines.wav"), streaming = False),
                "WIN":  pyglet.resource.media(os.path.join("audio", "The Descent.wav"), streaming = False),
                "GAME":     pyglet.resource.media(os.path.join("audio", "Trepidation.wav"), streaming = False),
                "TALE":     pyglet.resource.media(os.path.join("audio", "Fallen Angels.wav"), streaming = False),
                "LAST":     pyglet.resource.media(os.path.join("audio", "Inferno.wav"), streaming = False)}
