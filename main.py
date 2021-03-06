import sys, os, time
import pygame as pg

from puzzle import *
from solver import *

# global variables because I can't be bothered

def clamp(val, minv, maxv):
    return max(minv, min(val, maxv))

def reinit(puzzle, dimx, dimy):
    puzzle.__init__((dimx, dimy), (300, 300), 5)

def main():
    pg.init()
    pg.display.set_caption('VAI Puzzle')
    screen = pg.display.set_mode((300,300))
    clock = pg.time.Clock()
    dimx = 3
    dimy = 3
    puzzle = puzzle = Puzzle((dimx, dimy), (300, 300), 5)
    finalTiles = puzzle.tiles.copy()
    solver = PuzzleSolver(puzzle.gridSize, puzzle.tiles, finalTiles)

    sequence = []
    while True:
        dt = clock.tick()/100

        screen.fill((0,0,0))
        puzzle.draw(screen)
        pg.display.flip()

        if sequence and not puzzle.moving():
            move = sequence.pop()
            if move == 'U':
                puzzle.move(pg.K_UP)
            elif move == 'D':
                puzzle.move(pg.K_DOWN)
            elif move == 'L':
                puzzle.move(pg.K_LEFT)
            elif move == 'R':
                puzzle.move(pg.K_RIGHT)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)
            if not sequence and not puzzle.moving(): #react to events only if not moving in a sequence
                if event.type == pg.MOUSEBUTTONDOWN:
                    puzzle.click(pg.mouse.get_pos())
                    print(puzzle.tiles)
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT):
                        puzzle.move(event.key)
                    if event.key == pg.K_SPACE:
                        puzzle.random()
                    if event.key == pg.K_b:
                        solver = PuzzleSolver(puzzle.gridSize, puzzle.tiles, finalTiles)
                        sequence = solver.bfs()
                        dt = clock.tick()/100
                    if event.key == pg.K_a:
                        solver = PuzzleSolver(puzzle.gridSize, puzzle.tiles, finalTiles)
                        sequence = solver.aStar()
                        dt = clock.tick()/100
                    if event.key == pg.K_KP6:
                        dimx = clamp(dimx+1, 2, 6)
                        reinit(puzzle, dimx, dimy)
                        finalTiles = puzzle.tiles.copy()                       
                    if event.key == pg.K_KP4:
                        dimx = clamp(dimx-1, 2, 6)
                        reinit(puzzle, dimx, dimy)
                        finalTiles = puzzle.tiles.copy()
                    if event.key == pg.K_KP2:
                        dimy = clamp(dimy+1, 2, 6)
                        reinit(puzzle, dimx, dimy)
                        finalTiles = puzzle.tiles.copy()
                    if event.key == pg.K_KP8:
                        dimy = clamp(dimy-1, 2, 6)
                        reinit(puzzle, dimx, dimy)
                        finalTiles = puzzle.tiles.copy()
        puzzle.update(dt)



if __name__ == "__main__":
    main()