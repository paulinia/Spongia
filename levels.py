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
        global size_real
        self.level_id = level_id
        self.static_batch = pyglet.graphics.Batch()
        self.entities_batch = pyglet.graphics.Batch()
        self.blockes_batch = pyglet.graphics.Batch()
        self.camera = camera.Camera(width, height, (size, size), 2)
        self.blockers = {}
        self.characters = []
        
        with open("levels/" + str(self.level_id) + "level.data", "r") as f:
            data = f.readlines()
            i = 0
            mode = "N"
            for line in data:
                if i == 0:
                    self.n, self.distance, self.one, self.two, self.three = map(int, line.split())
                    self.mapa = [[] for i in range(self.n)]
                    self.tiles = [[] for i in range(self.n)]
                elif i <= self.n:
                    self.mapa[i - 1] = list(map(int, line.split()))
                    self.tiles[i - 1] = [(static.Wall((i - 1) * size_real, j * size_real, self.static_batch) if self.mapa[i - 1][j] == 3 else (static.Tile((i - 1) * size_real, j * size_real, self.static_batch) if self.mapa[i - 1][j] < 2 else None)) for j in range(self.n)]
                else:
                    if mode == "N":
                        if line[:3] == "END":
                            mode = "C"
                            continue
                        x, y, mater = line.split()
                        x = int(x)
                        y = int(y)
                        if self.mapa[x][y] == 1:
                            self.blockers[(x, y)] = static.Blocker(x * size_real, y * size_real, self.blockes_batch, mater)
                        else:
                            self.tiles[x][y] = static.Clothing(x * size_real, y * size_real, self.blockes_batch, mater)
                    elif mode == "C":
                        if line[:3] == "END":
                            mode = "P"
                            continue
                        
                        x, y, score, name, direct = line.split()
                        x = int(x)
                        y = int(y)
                        self.characters.append(characters.Person(name, x, y, self.entities_batch, score, direct))
                    else:
                        x, y = map(int, line.split())
                        self.player = player.Player(x, y, self.entities_batch)
                i += 1
       
    def draw(self):
        self.static_batch.draw()
        self.blockes_batch.draw()
        self.entities_batch.draw()
        if self.player.clothing == "blind":
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0, width, height, 0, height)), ('c4B', (0, 0, 0, min(255, 250)) * 4))
        
    def step(self, key):
        if key in D.keys():
            self.player.step(D[key], self)
            for person in self.characters:
                person.move(self)
        else:
            return self.explosion()
    
    def can_move(self, position_new, di):
        dx, dy = di
        nx, ny = position_new
        if self.mapa[nx][ny] == 3:
            return (False, "")
        if self.mapa[nx][ny] == 2:
            return (True, self.tiles[nx][ny].material, self.entities_batch)
        if self.mapa[nx][ny] == 1:
            if self.mapa[nx + dx][ny + dy] == 0 and self.blockers[(nx, ny)].material == self.player.clothing:
                can = True
                for person in self.characters:
                    if person.x == nx + dx and person.y == ny + dy:
                        can = False
                        break
                if not can:
                    return (False, "")
                self.mapa[nx + dx][ny + dy] = 1
                self.mapa[nx][ny] = 0
                block = self.blockers.pop((nx, ny))
                block.move(di)
                self.blockers[(nx + dx, ny + dy)] = block
                return (True, "")
            else:
                return (False, "")
        return (True, "")
    
    def blocked(self, position_new):
        nx, ny = position_new
        if self.mapa[nx][ny] == 0 or self.mapa[nx][ny] == 2:
            return (True, None)
        second = None
        if self.mapa[nx][ny] == 1:
            if self.blockers[(nx, ny)].material == "stop":
                second = "stop"
            if self.blockers[(nx, ny)].material == "turn":
                second = "turn"
        return (False, second)
    
    def explosion(self):
        if self.player.clothing == "stop":
            if self.mapa[self.player.x][self.player.y] != 2:
                self.mapa[self.player.x][self.player.y] = 1
                self.blockers[(self.player.x, self.player.y)] = static.Blocker(self.player.x * size_real, self.player.y * size_real, self.blockes_batch, "stop")
            return None
        if self.player.clothing == "turn":
            if self.mapa[self.player.x][self.player.y] != 2:
                self.mapa[self.player.x][self.player.y] = 1
                self.blockers[(self.player.x, self.player.y)] = static.Blocker(self.player.x * size_real, self.player.y * size_real, self.blockes_batch, "turn")
            return None
        if self.player.clothing == "spiral":
            score = self.spiral_explosion()
            if score < self.one:
                return (0, score)
            if score < self.two:
                return (1, score)
            if score < self.three:
                return (2, score)
            return (3, score)
        x, y = self.player.explode(self.entities_batch)
        cnt = 0
        for person in self.characters:
            if abs(x - person.x) + abs(y - person.y) <= self.distance:
                cnt += person.die(self.entities_batch)
        if cnt < self.one:
            return (0, cnt)
        if cnt < self.two:
            return (1, cnt)
        if cnt < self.three:
            return (2, cnt)
        return (3, cnt)
    
    def spiral_explosion(self):
        self.player.explode(self.entities_batch)
        score = 0
        was_there = [[False for i in range(self.n)] for j in range(self.n)]
        queue = [(self.player.x, self.player.y)]
        was_there[self.player.x][self.player.y] = True
        while len(queue) > 0:
            x, y = queue.pop(0)
            for dx, dy in DR:
                print("{};{} - {}".format(x + dx, y + dy, self.n))
                print("{}\n{}".format(self.mapa, was_there))
                if self.mapa[x + dx][y + dy] != 3 and self.mapa[x + dx][y + dy] != 1 and (not was_there[x + dx][y + dy]):
                    was_there[x + dx][y + dy] = 1
                    queue.append((x + dx, y + dy))
        
        for person in self.characters:
            if was_there[person.x][person.y]:
                score += person.die(self.entities_batch)
        return score
        
