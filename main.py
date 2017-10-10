from constants import *
import camera
import levels
from pyglet.gl import *

window = pyglet.window.Window(caption = "Amaz'hany",
                              width = width,
                              height = height)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
window.set_mouse_visible(True)

class GameState:
    def __init__(self):
        self.current_level = 1
        self.level = levels.Level(self.current_level)
        
    def draw(self):
        self.level.draw()
    
    def update(self, dt):
        return "GAME"
    
    def key_press(self, key):
        self.level.step(key)
        return "GAME"

states = {"GAME" : GameState()}

current = "GAME"

@window.event
def on_draw():
    global current
    window.clear()
    states[current].draw()
    
@window.event
def on_key_press(symbol, modifiers):
    global current
    if not symbol in pressed.keys():
        return None
    if pressed[symbol]:
        pass
    else:
        pressed[symbol] = True
        current = states[current].key_press(symbol)

@window.event
def on_key_release(symbol, modifiers):
    pressed[symbol] = False



accum = 0

def update(dt):
    global current, accum
    accum += dt
    
    while accum >= STEP:
        current = states[current].update(STEP)
        accum -= STEP
    window.set_caption("Amaz'hany [" + str(int(1 / dt)) + "]")

pyglet.clock.schedule_interval(update, 1 / FPS)

pyglet.app.run()
