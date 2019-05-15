import time
import numpy as np
from collections import deque
from queue import PriorityQueue

class State:
   def __init__(self, grid, emptyPosition = None, prev = None, move = None, dist = 0, heur = None):
      self.grid = grid
      if emptyPosition == None:
         self.emptyPosition = np.where(grid == 0)
      else:
         self.emptyPosition = emptyPosition
      self.prev = prev
      self.move = move
      self.dist = dist
      self.heuristics = heur

   # lt and gt are deliberately swapped so that PriorityQueue sorts lowest last
   def __lt__(self,other):
      return (self.heuristics + self.dist < other.heuristics + other.dist)

   def __le__(self,other):
      return(self.heuristics + self.dist <= other.heuristics + other.dist)

   def __gt__(self,other):
      return(self.heuristics + self.dist > other.heuristics + other.dist)

   def __ge__(self,other):
      return(self.heuristic + self.dist >= other.heuristics + other.dist)


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
      return [State(self.swap(state.grid, dir[1], (y, x)), emptyPosition=dir[1], prev=state, move=dir[0], dist=state.dist+1) for dir in directions]


   def reconstructGrid(self, tiles):
      grid = np.zeros((self.gridSize[1], self.gridSize[0]), dtype='int')
      for i in range(self.gridSize[0]*self.gridSize[1]):
         grid[tuple(reversed(tiles[i]))] = i+1
      grid[tuple(reversed(tiles[i]))] = 0
      return grid


   def inList(self, state, statelist):
      idx = 0
      for s in statelist:
         if (state.grid == s.grid).all():
            return True, idx
         idx += 1
      return False, 0


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
            print("Searched: ", len(self.closed), " states.")
            print("Search took: ", time.time() - then, " seconds.")
            return path
         
         neighbors = self.getNeighbors(state)
         for neighbor in neighbors:
            if self.inList(neighbor, self.open)[0] or self.inList(neighbor, self.closed)[0]:
               continue
            self.open.append(neighbor)

   def aStar(self):
      self.open = PriorityQueue()
      initstate = State(self.grid, dist = 0)
      initstate.heuristics = self.computeHeuristics(initstate)
      self.open.put(initstate)
      then = time.time()

      while not self.open.empty():
         state = self.open.get()
         self.closed.append(state)

         if(state.grid == self.finalState.grid).all():
            path = []
            while(state.prev != None):
               path.append(state.move)
               state = state.prev
            print("Searched: ", len(self.closed), " states.")
            print("Search took: ", time.time() - then, " seconds.")
            return path

         neighbors = self.getNeighbors(state)
         for neighbor in neighbors:
            neighbor.heuristics = self.computeHeuristics(neighbor)
            inlist, idx = self.inList(neighbor, self.closed)
            if inlist:
               if self.closed[idx] > neighbor:
                  neighbor = self.closed.pop(idx)
               else:
                  continue
            self.open.put(neighbor)



if __name__ == "__main__":

   tiles = [(1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1)]
   finaltiles = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
   solver = PuzzleSolver((2, 3), tiles, finaltiles)

   ### SOLVER TEST
   print("Runnung bfs")
   path = solver.bfs()
   print(path,"\n")

   solver = PuzzleSolver((2, 3), tiles, finaltiles)
   print("Running astar")
   path = solver.aStar()
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


   # while not q.empty():
   #    next_item = q.get()
   #    print(next_item.move)



