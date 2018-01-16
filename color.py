import colorsys
from collections import namedtuple
import random
import cmath

class Color(namedtuple('Color', ['hue', 'saturation', 'value'])):
    def to_int(self):
        r, g, b = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
        return (255 << 24) | (int(255 * g) << 16) | (int(255 * r) << 8) | int(255 * b)

    def mul_saturation(self, factor):
        return Color(self.hue, self.saturation * factor, self.value)

    def mul_value(self, factor):
        return Color(self.hue, self.saturation, self.value * factor)

    @staticmethod
    def random_color():
        return Color(random.uniform(0, 1), 1, 1)

    @staticmethod
    def average_color(colors):
        hue_sum = 0
        for color in colors:
            hue_sum += cmath.exp(1j * (color.hue - 0.5) * 2 * cmath.pi)
        return Color(
            cmath.phase(hue_sum / len(colors)) / (2 * cmath.pi) + 0.5,
            1, 1)
