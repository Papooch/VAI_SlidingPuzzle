import sys, os, time
import pygame as pg

from puzzle import *
from solver import *


def main():
    pg.init()
    pg.display.set_caption('Puzzle')
    screen = pg.display.set_mode((300,300))
    clock = pg.time.Clock()
    puzzle = Puzzle((3, 3), (300, 300), 5)
    finalTiles = puzzle.tiles.copy()
    #solver = PuzzleSolver(puzzle.gridSize, puzzle.tiles, puzzle.tiles)
    #solver.print()
    path = []

    print(puzzle.tiles)

    while True:
        dt = clock.tick()/1000

        screen.fill((0,0,0))
        puzzle.draw(screen)
        pg.display.flip()

        if path:
            move = path.pop()
            if move == 'U':
                puzzle.move(pg.K_UP)
            elif move == 'D':
                puzzle.move(pg.K_DOWN)
            elif move == 'L':
                puzzle.move(pg.K_LEFT)
            elif move == 'R':
                puzzle.move(pg.K_RIGHT)
            time.sleep(.1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)
            if event.type == pg.MOUSEBUTTONDOWN:
                puzzle.update(pg.mouse.get_pos())
                print(puzzle.tiles)
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT):
                    puzzle.move(event.key)
                if event.key == pg.K_SPACE:
                    puzzle.random()
                if event.key == pg.K_RETURN:
                    solver = PuzzleSolver(puzzle.gridSize, puzzle.tiles, finalTiles)
                    path = solver.bfs()




            

        




if __name__ == "__main__":
    main()