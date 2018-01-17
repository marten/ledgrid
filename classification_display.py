#!/usr/bin/python2
import time
import random
import json

from display import Display
from color import Color
from pusher import PusherWrapper
from waves import Grid, Cell

ROWS = 10
COLS = 20

class Main(object):
    def __init__(self):
        self.pusher = PusherWrapper()
        self.pusher.callback = lambda data: self.pusher_callback(data)
        self.display = Display(ROWS, COLS)
        self.display.begin()
        self.events = []
        self.grid = Grid(COLS, ROWS)

    def run(self):
        self.pusher.connect()
        t = time.clock()

        while True:
            # if random.random() > 0:
            #     self.events.append({"project_id": random.randint(1, 3000)})
            next_t = time.clock()
            delta_t = next_t - t

            self.calculate_waves(delta_t)
            if len(self.events) > 0:
                self.add_drops(self.events)
                self.events = []
            self.render()
            time.sleep(0.1)
            t = next_t

    def render(self):
        self.grid.render_onto(self.display)
        self.display.show()

    def add_drops(self, events):
        for event in events:
            print event
            project_id = event["project_id"]

            hue = (int(project_id) % 256) / 256.0
            color = Color(hue, 1.0, 1.0)
            row = random.randint(0, ROWS-1)
            col = random.randint(0, COLS-1)
            self.grid.set(col, row, Cell(color))

        print("")

    def calculate_waves(self, delta_t):
        self.grid = self.grid.advance(delta_t)
        pass

    def pusher_callback(self, data):
        self.events.append(json.loads(data))

if __name__ == '__main__':
    Main().run()
