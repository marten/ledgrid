#!/usr/bin/python2

import colorsys
import math
import random
import time

from collections import namedtuple

from display import Display

ROWS = 10
COLS = 20

rand = random.Random()

class Color(namedtuple('Color', ['red', 'green', 'blue'])):
    def to_int(self):
        return (255 << 24) | (self.green << 16) | (self.red << 8) | self.blue

    def __mul__(self, factor):
        def d(c):
            return min(255, max(0, int(factor * c)))
        return Color(d(self.red), d(self.green), d(self.blue))


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


FONT_STRING = """
 #   #   #  ###   # ###  #  ###  #   #    
# # ##  # #   #  ## #   #     # # # # # # 
# #  #    #  #  # # ##  ##    #  #   ##   
# #  #   #    # ###   # # #  #  # #   #   
# #  #  #     #   #   # # #  #  # #   # # 
 #  ### ### ##    # ##   #   #   #  ##   
000 111 222 333 444 555 666 777 888 999 :
"""

class Font:
    def __init__(self, font_string):
        lines = [line for line in font_string.split('\n') if len(line) > 0]
        chars = lines.pop()
        self.chars = {}
        for col in range(len(chars)):
            char = chars[col]
            if char == ' ':
                continue
            if char not in self.chars:
                self.chars[char] = [[] for row in range(len(lines))]
            char_matrix = self.chars[char]
            for row in range(len(lines)):
                char_matrix[row].append(lines[row][col] != ' ')

    def draw_text(self, grid, row, col, text):
        for char in text:
            char_matrix = self.chars[char]
            char_width = 0
            for r in range(len(char_matrix)):
                char_row = char_matrix[r]
                char_width = max(char_width, len(char_row))
                for c in range(len(char_row)):
                    if char_row[c]:
                        grid.spawn(Coords(row + r, col + c), Cell())
            col += char_width + 1

FONT = Font(FONT_STRING)

def draw_clock():
    grid = Grid()
    text = time.strftime('%H:%M')
    FONT.draw_text(grid, 2, 2, text)
    return grid


def render_grid(grid, display, brightness):
    for row in range(ROWS):
        for col in range(COLS):
            coords = Coords(row, col)
            display.set(row, col, grid[coords].color * brightness if coords in grid else Color(0, 0, 0))
    display.show()


class Main(object):
    def __init__(self):
        self.grid = Grid()
        self.display = Display(ROWS, COLS)
        self.display.begin()

    def render(self, brightness=1):
        render_grid(self.grid, self.display, math.pow(brightness, 3.0))
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
