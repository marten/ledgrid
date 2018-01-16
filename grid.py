from collections import namedtuple
import random
import math
from color import Color

class Coords(namedtuple('Coords', ['row', 'col'])):
    def neighbors(self):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr != 0 or dc != 0:
                    yield Coords(self.row + dr, self.col + dc)

class Cell(object):
    def __init__(self, color=None, age=0):
        if color is None:
            color = Color.random_color()
        self.color = color
        self.age = age

    def happy_birthday_to_me(self):
        return Cell(self.color, self.age + 1)


class Grid:
    def __init__(self, rows, cols, radiation):
        self.rows = rows
        self.cols = cols
        self.radiation = radiation
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

    def colors_neighbors(self, coords):
        return [self[c].color for c in coords.neighbors() if c in self]


    def advance(self):
        new_grid = Grid(self.rows, self.cols, self.radiation)
        for row in range(self.rows):
            for col in range(self.cols):
                coords = Coords(row, col)
                num_neighbors = self.count_neighbors(coords)
                if coords in self:
                    if 2 <= num_neighbors <= 3:
                        new_grid.spawn(coords, self[coords].happy_birthday_to_me())
                else:
                    if num_neighbors == 3:
                        new_grid.spawn(coords, Cell( Color.average_color(
                            self.colors_neighbors(coords) + self.radiation*[Color.random_color()]
                            ) ))
        return new_grid

    def render_onto(self, display, brightness):
        for row in range(self.rows):
            for col in range(self.cols):
                coords = Coords(row, col)
                color = self[coords].color if coords in self else Color(0, 0, 0)
                display.set(row, col, color.mul_saturation(math.pow(brightness, 0.5)).mul_value(math.pow(brightness, 3.0)))

    def is_empty(self):
        return len(self._cells) == 0

    def fingerprint(self):
        f = 0
        for row in range(self.rows):
            for col in range(self.cols):
                f = f << 1
                if Coords(row, col) in self:
                    f = f | 1
        return f

    def randomize(self):
        self.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                if random.randint(0, 1):
                    self.spawn(Coords(row, col), Cell())
