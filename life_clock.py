#!/usr/bin/python2
import math
import time

from collections import namedtuple

from display import Display
from color import Color
from font import FONT
from grid import Coords, Cell, Grid

ROWS = 10
COLS = 20
RADIATION = 1

def draw_clock():
    grid = Grid(ROWS, COLS, RADIATION)
    text = time.strftime('%H:%M')
    FONT.draw_text(grid, 2, 2, text)
    return grid


def render_grid(grid, display, brightness):
    for row in range(ROWS):
        for col in range(COLS):
            coords = Coords(row, col)
            color = grid[coords].color if coords in grid else Color(0, 0, 0)
            display.set(row, col, color.mul_saturation(math.pow(brightness, 0.5)).mul_value(math.pow(brightness, 3.0)))
    display.show()


class Main(object):
    def __init__(self):
        self.grid = Grid(ROWS, COLS, RADIATION)
        self.display = Display(ROWS, COLS)
        self.display.begin()

    def render(self, brightness=1):
        render_grid(self.grid, self.display, brightness)
        self.display.show()

    def run(self):
        while True:
            self.show_clock()
            self.apply_game_of_life()

    def show_clock(self):
        self.grid = draw_clock()
        for brightness in range(1, 11):
            self.render(brightness / 10.0)
            time.sleep(0.1)
        time.sleep(2.7)

    def apply_game_of_life(self):
        seen_fingerprints = set()
        brightness = 1
        while brightness >= 0:
            self.render(brightness)
            time.sleep(0.1)
            self.grid = self.grid.advance()
            if self.grid.fingerprint() in seen_fingerprints:
                brightness -= 0.05
            seen_fingerprints.add(self.grid.fingerprint())


if __name__ == '__main__':
    Main().run()
