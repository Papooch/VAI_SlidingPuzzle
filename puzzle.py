import pygame as pg
import random

class Puzzle:
   def __init__(self, gridSize, dimensions, tileSpacing):
      self.gridSize = gridSize
      self.tileSize = [dimensions[0]/gridSize[0] - tileSpacing*((gridSize[0]+1)/gridSize[0]),\
                        dimensions[1]/gridSize[1] - tileSpacing*((gridSize[1]+1)/gridSize[1])]
      self.tileSpacing = tileSpacing
      self.noOfTiles = gridSize[0]*gridSize[1]-1
      self.tiles = [(x, y) for y in range(gridSize[1]) for x in range(gridSize[0])]
      self.tilescoords = {(x,y):(x*(self.tileSize[0]+tileSpacing)+tileSpacing, y*(self.tileSize[1]+tileSpacing)+tileSpacing)
                           for y in range(gridSize[1]) for x in range(gridSize[0])}
      self.tilescoordsActual = [(x*(self.tileSize[0]+tileSpacing)+tileSpacing, y*(self.tileSize[1]+tileSpacing)+tileSpacing)
                                 for y in range(gridSize[1]) for x in range(gridSize[0])]
      self.prevTile = None
      self.speed = 200

      # generate images with numbers
      self.images = []
      self.font = pg.font.Font(None, int(self.tileSize[1]))
      for i in range(self.noOfTiles):
         image = pg.Surface((self.tileSize[0], self.tileSize[1]))
         image.fill((0, 0, 255))
         text = self.font.render(str(i+1), 2, (0, 0, 0))
         w, h = text.get_size()
         image.blit(text, ((self.tileSize[0]-w+tileSpacing)/2, (self.tileSize[1]-h+tileSpacing)/2))
         self.images.append(image)


   def getEmpty(self): return self.tiles[-1]
   def setEmpty(self, pos): self.tiles[-1] = pos
   emptyTile = property(getEmpty, setEmpty)


   def draw(self, screen):
      for i in range(self.noOfTiles):
         x, y = self.tilescoordsActual[i]
         screen.blit(self.images[i], (x, y))


   def inGrid(self, tile):
      return tile[0]>=0 and tile[0]<self.gridSize[0] and tile[1]>=0 and tile[1]<self.gridSize[1] and tile!=self.tiles[-1]


   def adjacent(self):
      x, y = self.emptyTile
      return [a for a in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)) if self.inGrid(a)]
      #return ((x-1, y), (x+1, y), (x, y-1), (x, y+1))


   def random(self):
      adj = [pos for pos in self.adjacent() if self.inGrid(pos) and pos != self.prevTile]
      self.swap(random.choice(adj))


   def click(self, mpos):
      tile = (mpos[0]//(self.tileSize[0]+self.tileSpacing), mpos[1]//(self.tileSize[1]+self.tileSpacing))
      if tile in self.adjacent():
         self.swap(tile)


   def update(self, dt):
      ds = self.speed*dt
      for i in range(self.noOfTiles):
         x, y = self.tilescoordsActual[i]
         fx, fy = self.tilescoords[self.tiles[i]]
         dx = fx-x
         dy = fy-y
         if dx > self.tileSpacing: x += ds
         elif dx < -self.tileSpacing: x -= ds
         else: x = fx


         if dy > self.tileSpacing: y += ds
         elif dy < -self.tileSpacing: y -= ds
         else: y = fy
         self.tilescoordsActual[i] = x, y


   def moving(self):
      for i in range(self.noOfTiles):
         x, y = self.tilescoordsActual[i]
         fx, fy = self.tilescoords[self.tiles[i]]
         if x != fx or y != fy:
            return True
      return False


   def swap(self, tile):
      n = self.tiles.index(tile)
      self.tiles[n], self.emptyTile, self.prevTile = self.emptyTile, self.tiles[n], self.emptyTile


   def move(self, dir):
      x,y = self.emptyTile
      if dir == pg.K_UP:
         tile = x, y+1
      elif dir == pg.K_DOWN:
         tile = x, y-1
      elif dir == pg.K_LEFT:
         tile = x+1, y
      elif dir == pg.K_RIGHT:
         tile = x-1, y
      
      if self.inGrid(tile):
         self.swap(tile)
