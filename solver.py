import numpy as np

class State:
   def __init__(self, )
      pass

class PuzzleSolver:
   def __init__(self, gridSize):
      self.gridSize = gridSize
      self.grid = np.zeros((gridSize[1], gridSize[0]), dtype='int')
      self.open = []
      self.closed = []

   def neighborState(self, state):


   def reconstructGrid(self, tiles):
      grid = np.zeros((self.gridSize[1], self.gridSize[0]), dtype='int')
      for i in range(self.gridSize[0]*self.gridSize[1]):
         grid[tuple(reversed(tiles[i]))] = i+1
      grid[tuple(reversed(tiles[i]))] = 0
      print(grid)


   def printGrid(self):
      print(self.grid)