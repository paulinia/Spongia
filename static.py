from constants import *

class Tile:
    def __init__(self, x, y, batch):
        self.tile_imag = pyglet.resource.image(os.path.join("graphics", "squareTile.png"))
        self.tile_imag.anchor_x = 0
        self.tile_imag.anchor_y = 0
        self.sprite = pyglet.sprite.Sprite(self.tile_imag, x = x, y = y, usage = 'static', batch = batch)
        self.sprite.scale = (size_real / size)
    
class Wall:
    def __init__(self, x, y, batch):
        self.tile_imag = pyglet.resource.image(os.path.join("graphics", "wall.png"))
        self.tile_imag.anchor_x = 0
        self.tile_imag.anchor_y = 0
        self.sprite = pyglet.sprite.Sprite(self.tile_imag, x = x, y = y, usage = 'static', batch = batch)
        self.sprite.scale = (size_real / size)
    
class Clothing:
    def __init__(self, x, y, batch, material="TNT"):
        self.tile_imag = pyglet.resource.image(os.path.join("graphics", material + "cloth.png"))
        self.tile_imag.anchor_x = 0
        self.tile_imag.anchor_y = 0
        self.material = material
        self.sprite = pyglet.sprite.Sprite(self.tile_imag, x = x, y = y, usage = 'static', batch = batch)
        self.sprite.scale = (size_real / size)
        
class Blocker:
    def __init__(self, x, y, batch, material="TNT"):
        self.material = material
        self.tile_imag = pyglet.resource.image(os.path.join("graphics", material + "B.png"))
        self.tile_imag.anchor_x = 0
        self.tile_imag.anchor_y = 0
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(self.tile_imag, x = x, y = y, batch = batch)
        self.sprite.scale = (size_real / size)
        
    def move(self, di):
        self.x += di[0] * size_real
        self.y += di[1] * size_real
        self.sprite.set_position(self.x, self.y)
