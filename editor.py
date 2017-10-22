from constants import *
import os

class Level:
    def create_level(self, path):
        self.path = path
        self.n = int(input("Rozmer levelu: "))
        self.distance = int(input("Attack distance: "))
        self.scores = list(map(int, input("Scores for stars: ").split()))
        self.mapa = [[0 for y in range(self.n)] for x in range(self.n)]
        self.walls = [[None for y in range(self.n)] for x in range(self.n)]
        self.wall_pics = [["." for y in range(self.n)] for x in range(self.n)]
        self.characters = [[None for y in range(self.n)] for x in range(self.n)]
        self.chardirs = [[None for y in range(self.n)] for x in range(self.n)]
        tile_image = pyglet.resource.image("graphics/squareTile.png")
        self.wall_image = pyglet.resource.image("graphics/wall.png")
        self.player_pos = (0, 0)
        self.player = None
        self.batch_tiles = pyglet.graphics.Batch()
        self.batch_static = pyglet.graphics.Batch()
        self.batch_entity = pyglet.graphics.Batch()
        self.static = []
        self.static_mat = {}
        for i in range(self.n):
            for j in range(self.n):
                self.static.append(pyglet.sprite.Sprite(tile_image, x = j * size, y = i * size, batch = self.batch_tiles))
    
    def load_level(self, path):
        self.path = path
        self.batch_tiles = pyglet.graphics.Batch()
        self.batch_static = pyglet.graphics.Batch()
        self.batch_entity = pyglet.graphics.Batch()
        self.static = []
        self.static_mat = {}
        tile_image = pyglet.resource.image("graphics/squareTile.png")
        self.wall_image = pyglet.resource.image("graphics/wall.png")
        print(path + "level.data")
        with open(path + "level.data", "r") as f:
            data = f.readlines()
            i = 0
            mode = "N"
            for line in data:
                print("line je {} and mode is {}".format(line[:-1], mode))
                if i == 0:
                    self.n, self.distance, one, two, three = map(int, line.split())
                    self.scores = [one, two, three]
                    self.mapa = [[] for i in range(self.n)]
                    self.walls = [[None for y in range(self.n)] for x in range(self.n)]
                    self.characters = [[None for y in range(self.n)] for x in range(self.n)]
                    self.chardirs = [[None for y in range(self.n)] for x in range(self.n)]
                    for l in range(self.n):
                        for j in range(self.n):
                            self.static.append(pyglet.sprite.Sprite(tile_image, x = l * size, y = j * size, batch = self.batch_tiles))
                elif i <= self.n:
                    self.mapa[i - 1] = list(map(int, line.split()))
                    print(self.mapa[i - 1])
                    self.walls[i - 1] = [(pyglet.sprite.Sprite(self.wall_image, x = (i - 1) * size, y = j * size, batch = self.batch_static) if self.mapa[i - 1][j] == 3 else None) for j in range(self.n)]
                else:
                    if mode == "N":
                        if line[:3] == "END":
                            mode = "C"
                            continue
                        x, y, mater = line.split()
                        x = int(x)
                        y = int(y)
                        self.static_mat[(x, y)] = mater
                        self.walls[x][y] = pyglet.sprite.Sprite(pyglet.resource.image("graphics/" + mater + ("B" if self.mapa[x][y] == 1 else "cloth") + ".png"), x = x * size, y = y * size, batch = self.batch_static)
                    elif mode == "C":
                        if line[:3] == "END":
                            mode = "P"
                            continue
                        x, y, score, name, direct = line.split()
                        x = int(x)
                        y = int(y)
                        self.chardirs[int(x)][int(y)] = (score, name, direct)
                        image = pyglet.resource.image("graphics/" + name + ".png")
                        self.characters[int(x)][int(y)] = pyglet.sprite.Sprite(image, x = x * size, y = y * size, batch = self.batch_static)
                    else:
                        x, y = map(int, line.split())
                        self.player_pos = (x, y)
                        image = pyglet.resource.image("graphics/Leather.png")
                        self.player = pyglet.sprite.Sprite(image, x = x * size, y = y * size, batch = self.batch_entity)
                i += 1
    
    def draw(self):
        self.batch_tiles.draw()
        self.batch_static.draw()
        self.batch_entity.draw()
    
    def key_press(self, mode):
        pass
    
    def add_entity(self, mode, x, y):
        print("Add entity on {} {} with mode {}".format(x, y, mode))
        try:
            if x < 0 or x >= self.n or y < 0 or y >= self.n:
                return
            if mode == "WALL":
                if (int(x), int(y)) in self.static_mat:
                    self.static_mat.pop((int(x), int(y)))
                self.walls[int(x)][int(y)] = pyglet.sprite.Sprite(self.wall_image, x = x * size, y = y * size, batch = self.batch_static)
                self.mapa[int(x)][int(y)] = 3
            if mode == "DEMOLISH":
                if self.walls[int(x)][int(y)] != None:
                    if (int(x), int(y)) in self.static_mat:
                        self.static_mat.pop((int(x), int(y)))
                    self.walls[int(x)][int(y)].delete()
                if self.characters[int(x)][int(y)] != None:
                    self.characters[int(x)][int(y)].delete()
                self.characters[int(x)][int(y)] = None
                self.walls[int(x)][int(y)] = None
                self.mapa[int(x)][int(y)] = 0
            if mode == 'BLOCKER':
                if (int(x), int(y)) in self.static_mat:
                    self.static_mat.pop((int(x), int(y)))
                btype = input("Enter type of blocker: ")
                image = pyglet.resource.image("graphics/" + btype + "B.png")
                self.walls[int(x)][int(y)] = pyglet.sprite.Sprite(image, x = x * size, y = y  * size, batch = self.batch_static)
                self.mapa[int(x)][int(y)] = 1
                self.static_mat[(int(x), int(y))] = btype
            if mode == 'CLOTH':
                if (int(x), int(y)) in self.static_mat:
                    self.static_mat.pop((int(x), int(y)))
                btype = input("Enter type of warderobe: ")
                image = pyglet.resource.image("graphics/" + btype + "cloth.png")
                self.walls[int(x)][int(y)] = pyglet.sprite.Sprite(image, x = x * size, y = y  * size, batch = self.batch_static)
                self.mapa[int(x)][int(y)] = 2
                self.static_mat[(int(x), int(y))] = btype
            if mode == 'PLAYER':
                image = pyglet.resource.image("graphics/Leather.png")
                self.player = pyglet.sprite.Sprite(image, x = x * size, y = y * size, batch = self.batch_entity)
                self.player_pos = (x, y)
            if mode == 'ENEMY':
                etype = input("Enter name of person: ")
                dire = input("Enter (in WASD) turining directions.: ")
                lives = input("Enter the score for this character.: ")
                self.chardirs[int(x)][int(y)] = (lives, etype, dire)
                image = pyglet.resource.image("graphics/" + etype + ".png")
                self.characters[int(x)][int(y)] = pyglet.sprite.Sprite(image, x = x * size, y = y * size, batch = self.batch_static)
        except:
            print("FAILED")
        
    def write_to_file(self):
        with open(self.path + "level.data", 'w') as lfile:
            lfile.write("{} {} {}\n".format(self.n, self.distance, " ".join(map(str, self.scores))))
            for i in range(self.n):
                lfile.write(" ".join(map(str, self.mapa[i])))
                lfile.write("\n")
            
            lfile.write("\n".join(["{} {} {}".format(poz[0], poz[1], name) for poz, name in self.static_mat.items()]))
            
            lfile.write("\nEND\n")
            for i in range(self.n):
                for j in range(self.n):
                    if self.characters[i][j] != None:
                        lfile.write("{} {} {} {} {}\n".format(i, j, self.chardirs[i][j][0], self.chardirs[i][j][1], self.chardirs[i][j][2]))
            lfile.write("END\n")
            lfile.write("{} {}".format(int(self.player_pos[0]), int(self.player_pos[1])))
            
            
                
