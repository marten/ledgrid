from collections import namedtuple
import random
import math
from color import Color

class Cell(object):
    def __init__(self, color=None, velocity=None):
        if color is None:
            color = Color.black()
        if velocity is None:
            velocity = (0, 0)
        self.color = color
        self.velocity = velocity

    def fade(self):
        return Cell(self.color.mul_value(0.9), self.velocity)

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        self.rows = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell()
                row.append(cell)
            self.rows.append(row)

    def get(self, x, y):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.rows[y][x]
        else:
            return Cell()

    def set(self, x, y, cell):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.rows[y][x] = cell

    def advance(self, delta_t):
        new_grid = Grid(self.width, self.height)

        for (x, y) in self.coords():
            cell = self.rows[y][x]

            neighbour_coords = [(x+dx, y+dy) for dx in range(-1, 1) for dy in range(-1, 1)]
            neighbours = [self.get(cx, cy) for (cx, cy) in neighbour_coords]
            neighbour_colors = [n.color for n in neighbours]

            new_cell = Cell(Color.average_color(neighbour_colors))

            new_grid.set(x, y, new_cell)


        return new_grid

    def render_onto(self, display):
        for (x, y) in self.coords():
            display.set(y, x, self.rows[y][x].color)

    def coords(self):
        return [(x, y) for x in range(self.width) for y in range(self.height)]
