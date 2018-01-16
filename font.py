import random
from color import Color
from grid import Coords, Cell

FONT_STRING = """
 #   #   #  ###   # ###  #  ###  #   #
# # ##  # #   #  ## #   #     # # # # # #
# #  #    #  #  # # ##  ##    #  #  # #
# #  #   #    # ###   # # #  #  # #  ##
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
                enabled = lines[row][col] != ' ' if col < len(lines[row]) else False
                char_matrix[row].append(enabled)

    def draw_text(self, grid, row, col, text):
        hue = random.uniform(0, 1)
        hue_step = random.uniform(-0.4, 0.4)
        for char in text:
            char_matrix = self.chars[char]
            char_width = 0
            char_color = Color(hue, 1, 1)
            hue = (hue + hue_step) % 1
            for r in range(len(char_matrix)):
                char_row = char_matrix[r]
                char_width = max(char_width, len(char_row))
                for c in range(len(char_row)):
                    if char_row[c]:
                        grid.spawn(Coords(row + r, col + c), Cell(char_color))
            col += char_width + 1

FONT = Font(FONT_STRING)
