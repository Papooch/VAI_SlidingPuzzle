import sys, os
import pygame as pg

from puzzle import *
from solver import *


def main():
    pg.init()
    pg.display.set_caption('Puzzle')
    screen = pg.display.set_mode((300,300))
    clock = pg.time.Clock()
    puzzle = Puzzle((2, 3), (300, 300), 5)
    solver = PuzzleSolver(puzzle.gridSize)
    solver.print()
    print(puzzle.tiles)

    while True:
        dt = clock.tick()/1000

        screen.fill((0,0,0))
        puzzle.draw(screen)
        pg.display.flip()

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
                solver.reconstructGrid(puzzle.tiles)

            

        




if __name__ == "__main__":
    main()