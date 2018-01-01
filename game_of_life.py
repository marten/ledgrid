#!/usr/bin/python2

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import colorsys
import math
import random
import time

from collections import namedtuple
from neopixel import *

rand = random.Random()


# LED strip configuration:
ROWS           = 10
COLS           = 20
LED_COUNT      = ROWS * COLS     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class Color(namedtuple('Color', ['red', 'green', 'blue'])):
    def to_int(self):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (255 << 24) | (self.green << 16) | (self.red << 8) | self.blue

    def __mul__(self, factor):
        def d(c):
            return min(255, max(0, int(factor * c)))
        return Color(d(self.red), d(self.green), d(self.blue))

class LedGrid:
    def __init__(self, width, height):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.width = width
        self.height = height

    def begin(self):
        self.strip.begin()

    def show(self):
        self.strip.show()

    def clear(self):
        for col in range(0, self.width):
            for row in range(0, self.height):
                self.set(row, col, Color(0, 0, 0))

    def set(self, row, col, color):
        self.strip.setPixelColor(self.index(row, col), color.to_int())

    def index(self, row, col):
        if row % 2 == 1:
            col = self.width - col - 1
        return row * self.width + col


class Coords(namedtuple('Coords', ['row', 'col'])):
    def neighbors(self):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr != 0 or dc != 0:
                    yield Coords(self.row + dr, self.col + dc)


class Cell(object):
    def __init__(self, color=None, age=0):
        if color is None:
            hue = rand.uniform(0, 1)
            saturation = 1
            value = 1
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            color = Color(r * 255, g * 255, b * 255)
        self.color = color
        self.age = age

    def happy_birthday_to_me(self):
        return Cell(self.color, self.age + 1)


class Grid:
    def __init__(self):
        self.clear()

    def clear(self):
        self._cells = {}

    def __getitem__(self, coords):
        return self._cells[coords]

    def __contains__(self, coords):
        return coords in self._cells

    def spawn(self, coords, cell):
        self._cells[coords] = cell

    def count_neighbors(self, coords):
        return len([c for c in coords.neighbors() if c in self])

    def advance(self):
        new_grid = Grid()
        for row in range(ROWS):
            for col in range(COLS):
                coords = Coords(row, col)
                num_neighbors = self.count_neighbors(coords)
                if coords in self:
                    if 2 <= num_neighbors <= 3:
                        new_grid.spawn(coords, self[coords].happy_birthday_to_me())
                else:
                    if num_neighbors == 3:
                        new_grid.spawn(coords, Cell())
        return new_grid

    def is_empty(self):
        return len(self._cells) == 0

    def fingerprint(self):
        f = 0
        for row in range(ROWS):
            for col in range(COLS):
                f = f << 1
                if Coords(row, col) in self:
                    f = f | 1 
        return f

    def randomize(self):
        self.clear()
        for row in range(ROWS):
            for col in range(COLS):
                if rand.randint(0, 1):
                    self.spawn(Coords(row, col), Cell())


def render_grid(grid, display, brightness):
    for row in range(ROWS):
        for col in range(COLS):
            coords = Coords(row, col)
            display.set(row, col, grid[coords].color * brightness if coords in grid else Color(0, 0, 0))
    display.show()
    

# Main program logic follows:
if __name__ == '__main__':
    seen_fingerprints = set()
    brightness = 1

    grid = Grid()
    grid.randomize()

    display = LedGrid(COLS, ROWS)
    display.begin()

    while True:
        render_grid(grid, display, math.pow(brightness, 3.0))
        if grid.fingerprint() in seen_fingerprints:
            brightness -= 0.05
        if grid.is_empty() or brightness <= 0:
            time.sleep(1.0)
            grid.randomize()
            seen_fingerprints = set()
            brightness = 1
        seen_fingerprints.add(grid.fingerprint())
        grid = grid.advance()
        time.sleep(0.1)
