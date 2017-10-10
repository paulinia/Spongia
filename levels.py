import pyglet
from constants import *
import camera
import static
import player
import random
import characters


class Level:
    def __init__(self, level_id):
        # not editor yet
        self.level_id = level_id
        self.n = 10
        self.static_batch = pyglet.graphics.Batch()
        self.entities_batch = pyglet.graphics.Batch()
        self.blockes_batch = pyglet.graphics.Batch()
        self.mapa = [[random.randint(0, 3) for j in range(self.n)] for i in range(self.n)]
        tiles = [static.Tile, static.Tile, static.Wall, static.Clothing]
        self.tiles = [[tiles[self.mapa[i][j]](j * size_real, i * size_real, self.static_batch) for j in range(self.n)] for i in range(self.n)]
        self.camera = camera.Camera(width, height, (size, size), 2)
        self.blockers = {}
        for i in range(self.n):
            for j in range(self.n):
                if self.mapa[i][j] == 1:
                    self.blockers[(j, i)] = (static.Blocker(j * size_real, i * size_real, self.blockes_batch, "TNT"))
        self.player = player.Player(random.randint(0, self.n - 1), random.randint(0, self.n - 1), self.entities_batch)
        self.characters = []
        for i in range(random.randint(2, 10)):
            self.characters.append(characters.Person("Man1", random.randint(0, self.n - 1), random.randint(0, self.n - 1), self.entities_batch))
        
    def draw(self):
        self.static_batch.draw()
        self.blockes_batch.draw()
        self.entities_batch.draw()
        
    def step(self, key):
        self.player.step(D[key], self)
    
    def can_move(self, position_new, di):
        dx, dy = di
        nx, ny = position_new
        if self.mapa[ny][nx] == 2:
            return (False, "")
        if self.mapa[ny][nx] == 3:
            return (True, self.tiles[ny][nx].material, self.entities_batch)
        if self.mapa[ny][nx] == 1:
            if self.mapa[ny + dy][nx + dx] == 0 and self.blockers[(nx, ny)].material == self.player.clothing:
                self.mapa[ny + dy][nx + dx] = 1
                self.mapa[ny][nx] = 0
                block = self.blockers.pop((nx, ny))
                block.move(di)
                self.blockers[(nx + dx, ny + dy)] = block
                return (True, "")
            else:
                return (False, "")
        return (True, "")
    
    def blocked(self, position_new):
        nx, ny = position_new
        if self.mapa[ny][nx] == 0 or self.mapa[ny][nx] == 3:
            return True
        return False
