import numpy as np
from collections import deque

class State:
   def __init__(self, grid, prev = None, move = None):
      self.grid = grid
      self.prev = prev
      self.move = move

class PuzzleSolver:
   def __init__(self, gridSize, initialtiles, finaltiles):
      self.gridSize = gridSize
      self.grid = self.reconstructGrid(initialtiles)
      self.open = deque()
      self.closed = []
      self.finalState = State(self.reconstructGrid(finaltiles))


   def inGrid(self, tile):
      return tile[0]>=0 and tile[0]<self.gridSize[1] and tile[1]>=0 and tile[1]<self.gridSize[0]


   def swap(self, grid, a, b):
      grid = grid.copy()
      tmp = grid[a]
      grid[a] = grid[b]
      grid[b] = tmp
      return grid


   def getNeighbors(self, state):
      #print("neighbors of:\n", state.grid)
      y, x = np.where(state.grid == 0) # coords of empty tile
      directions = [a for a in (("D", (y-1, x)), ("U", (y+1, x)), ("R", (y, x-1)), ("L", (y, x+1))) if self.inGrid(a[1])]
      return [State(self.swap(state.grid, dir[1], (y, x)), state, dir[0]) for dir in directions]


   def reconstructGrid(self, tiles):
      grid = np.zeros((self.gridSize[1], self.gridSize[0]), dtype='int')
      for i in range(self.gridSize[0]*self.gridSize[1]):
         grid[tuple(reversed(tiles[i]))] = i+1
      grid[tuple(reversed(tiles[i]))] = 0
      return grid


   def inList(self, state, statelist):
      for s in statelist:
         if (state.grid == s.grid).all():
            return True
      return False


   def printGrid(self):
      print(self.grid)


   def bfs(self):
      self.open.append(State(self.grid))
      
      while self.open:
         state = self.open.popleft()
         self.closed.append(state)

         if (state.grid == self.finalState.grid).all():
            path = []
            while(state.prev != None):
               path.append(state.move)
               state = state.prev
            return path

         neighbors = self.getNeighbors(state)
         for neighbor in neighbors:
            if self.inList(neighbor, self.open) or self.inList(neighbor, self.closed):
               continue
            self.open.append(neighbor)






if __name__ == "__main__":

   finaltiles = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
   tiles = [(1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1)]
   #tiles = [(0, 1), (0, 0), (1, 1), (1, 2), (0, 2), (1, 0)]
   #finaltiles = [(0, 0), (1, 0), (1, 1), (0, 1)]
   #tiles = [(1, 0), (1, 1), (0, 1), (0, 0)]

   solver = PuzzleSolver((2, 3), tiles, finaltiles)
   neighbors = (solver.getNeighbors(State(solver.grid)))

   print(solver.grid, "\n")

   for neighbor in neighbors:
      print(neighbor.grid, "\n")
   
   path = solver.bfs()
   print(path)


