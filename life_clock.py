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
FADE_STEPS = 32

def draw_clock():
    grid = Grid(ROWS, COLS, RADIATION)
    text = time.strftime('%H:%M')
    FONT.draw_text(grid, 2, 2, text)
    return grid

class Main(object):
    def __init__(self):
        self.grid = Grid(ROWS, COLS, RADIATION)
        self.display = Display(ROWS, COLS)
        self.display.begin()

    def run(self):
        while True:
            self.show_clock()
            self.apply_game_of_life()

    def render(self, brightness=1):
        self.grid.render_onto(self.display, brightness)
        self.display.show()

    def show_clock(self):
        self.grid = draw_clock()
        for brightness in range(1, FADE_STEPS):
            self.render(brightness / float(FADE_STEPS - 1))
        time.sleep(2.7)

    def apply_game_of_life(self):
        seen_fingerprints = set()
        brightness = 1
        grid_timestamp = time.clock()

        while brightness >= 0:
            now = time.clock()
            self.render(brightness)

            if (now - grid_timestamp) > 0.1:
                grid_timestamp = now

                seen_fingerprints.add(self.grid.fingerprint())
                self.grid = self.grid.advance()

            if self.grid.fingerprint() in seen_fingerprints:
                brightness -= (1.0 / float(FADE_STEPS))




if __name__ == '__main__':
    Main().run()
