from neopixel import *

# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class Display:
    def __init__(self, rows, cols):
        self.strip = Adafruit_NeoPixel(rows * cols, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.rows = rows
        self.cols = cols

    def begin(self):
        self.strip.begin()

    def show(self):
        self.strip.show()

    def clear(self):
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                self.set(row, col, Color(0, 0, 0))

    def set(self, row, col, color):
        self.strip.setPixelColor(self.index(row, col), color.to_int())

    def index(self, row, col):
        if row % 2 == 0:
            col = self.cols - col - 1
        return self.rows * self.cols - 1 - (row * self.cols + col)
