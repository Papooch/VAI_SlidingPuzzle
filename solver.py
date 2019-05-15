import time
import numpy as np
from collections import deque
from queue import PriorityQueue

class State:
   def __init__(self, grid, emptyPosition = None, prev = None, move = None, dist = None, heur = None):
      self.grid = grid
      if emptyPosition == None:
         self.emptyPosition = np.where(grid == 0)
      else:
         self.emptyPosition = emptyPosition
      self.prev = prev
      self.move = move
      self.distance = dist
      self.heuristics = heur

   def __lt__(self,other):
      return (self.heuristics < other.heuristics)

   def __le__(self,other):
      return(self.heuristics <= other.heuristics)

   def __gt__(self,other):
      return(self.heuristics > other.heuristics)

   def __ge__(self,other):
      return(self.heuristic >= other.heuristics)


class PuzzleSolver:
   def __init__(self, gridSize, initialtiles, finaltiles):
      self.gridSize = gridSize
      self.grid = self.reconstructGrid(initialtiles)
      self.open = []
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


   def emptyPosition(self, grid):
      return np.where(grid == 0)


   def computeHeuristics(self, state):
      current = state.grid.flatten().tolist()
      final = self.finalState.grid.flatten().tolist()
      heur = 0
      for tile in current:
         cidx = current.index(tile) # current tile index
         fidx = final.index(tile) # final tile index
         y, x = cidx // int(np.sqrt(len(current))), cidx % int(np.sqrt(len(current)))
         fy, fx = fidx // int(np.sqrt(len(current))), fidx % int(np.sqrt(len(current)))
         heur += (abs(y - fy) + abs(x - fx))
      return heur


   def getNeighbors(self, state):
      #print("neighbors of:\n", state.grid)
      #y, x = np.where(state.grid == 0)
      y, x = state.emptyPosition # # coords of empty tile #
      directions = [a for a in (("D", (y-1, x)), ("U", (y+1, x)), ("R", (y, x-1)), ("L", (y, x+1))) if self.inGrid(a[1])]
      return [State(self.swap(state.grid, dir[1], (y, x)), dir[1], state, dir[0]) for dir in directions]


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
      self.open = deque()
      self.open.append(State(self.grid))
      then = time.time()

      while self.open:
         state = self.open.popleft()
         self.closed.append(state)
         
         if (state.grid == self.finalState.grid).all():
            path = []
            while(state.prev != None):
               path.append(state.move)
               state = state.prev
            print("Searched: ", len(self.open), " states.")
            print("Search took: ", time.time() - then, " seconds.")
            return path
         
         neighbors = self.getNeighbors(state)
         for neighbor in neighbors:
            if self.inList(neighbor, self.open) or self.inList(neighbor, self.closed):
               continue
            self.open.append(neighbor)






if __name__ == "__main__":

   finaltiles = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
   tiles = [(0, 0), (1, 0), (0, 1), (1, 1), (1, 2), (0, 2)]

   #tiles = [(1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1)]
   #tiles = [(0, 1), (0, 0), (1, 1), (1, 2), (0, 2), (1, 0)]
   #finaltiles = [(0, 0), (1, 0), (1, 1), (0, 1)]
   #tiles = [(1, 0), (1, 1), (0, 1), (0, 0)]

   ### SOLVER TEST
   solver = PuzzleSolver((2, 3), tiles, finaltiles)

   print(solver.computeHeuristics(State(solver.grid)))
   # neighbors = (solver.getNeighbors(State(solver.grid, solver.emptyPosition(solver.grid))))

   # print(solver.grid, "\n")

   # for neighbor in neighbors:
   #    print(neighbor.grid, "\n")
   
   path = solver.bfs()
   print(path)

   ### PRIORITY QUEUE TEST
   # q = PriorityQueue()

   # st1 = State(tiles, move="A", heur=1)
   # st2 = State(tiles, move="B", heur=3)
   # st3 = State(tiles, move="C", heur=1)
   # st4 = State(tiles, move="D", heur=2)

   # q.put(st1)
   # q.put(st2)
   # q.put(st3)
   # q.put(st4)

   # del q.queue[1]

   # while not q.empty():
   #    next_item = q.get()
   #    print(next_item.move)



