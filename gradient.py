# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *


# LED strip configuration:
LED_COUNT      = 200     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (green << 16)| (red << 8) | blue

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
		self.strip.setPixelColor(self.index(row, col), color)

    def index(self, row, col):
        if row % 2 == 1:
            col = self.width - col - 1
        return row * self.width + col




# Main program logic follows:
if __name__ == '__main__':
    grid = LedGrid(20, 10)
    grid.begin()
    print("Press C-c to quit.")

    while True:
        for col in range(0, 20):
            for row in range(0, 10):
                print(row, col)
                grid.clear()
                grid.show()
                time.sleep(2)
                grid.set(row, col, Color(0, 0, 255))
                grid.show()
                time.sleep(2)




