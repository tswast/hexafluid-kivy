from __future__ import division

import kivy
kivy.require('1.5.1')

# here, activate monitor module for FPS
# from kivy.config import Config
# Config.set('modules', 'monitor', '')

import copy
from random import random
from math import sqrt
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty

import board


class Hexagon(Widget):
    tileradius = NumericProperty(1.0)
    density = NumericProperty(1.0)

    def __init__(self, is_filled, **kwargs):
        super(Hexagon, self).__init__(**kwargs)
        # Center + six sides
        if is_filled:
            self.densities = [ random() for i in xrange(7) ]
            #self.densities = [ 1, random(), 0, 0, 0, 0, 0 ]
        else:
            self.densities = [ 0 for i in xrange(7) ]
        self.propogated_densities = copy.copy(self.densities)
        self.recalculateDensity()

    def recalculateDensity(self):
        self.density = sum(self.densities) / len(self.densities)


class TileMap(RelativeLayout):
    def __init__(self, **kwargs):
        super(TileMap, self).__init__(**kwargs) # init ScatterPlane with above parameters

        # How many tiles to make? 32x64?
        tileradius = 8

        loaded_tiles = board.load_board()

        self.tiles = []
        for y_tile in xrange(64):
            row = []
            self.tiles.append(row)
            for x_tile in xrange(32):
                hexagon = Hexagon(
                    loaded_tiles[y_tile][x_tile],
                    pos=((x_tile+1) * 3 * tileradius + (y_tile % 2) * (1.5 * tileradius),
                        (y_tile+1) * 0.5 * sqrt(3) * tileradius),
                    size_hint=(1.0/64, 1.0/64))
                self.add_widget(hexagon)
                hexagon.tileradius = tileradius
                hexagon.height=(tileradius*sqrt(3))
                row.append(hexagon)

    def update(self, *args, **kwargs):
        self.do_propagation_step()
        self.do_collision_step()

    def do_propagation_step(self):
        for row_i, row in enumerate(self.tiles):
            for col_i, hexagon in enumerate(row):
                for i, density in enumerate(hexagon.densities):
                    if i == 0:
                        hexagon.propogated_densities[0] = density
                    elif i == 1:
                        # Top. Two rows above.
                        top_y = row_i - 2
                        if top_y < 0:
                            top_y += 64
                        self.tiles[top_y][col_i].propogated_densities[1] = density
                    elif i == 2:
                        # Top-right. One row above, one right (or same)
                        top_y = row_i - 1
                        if top_y < 0:
                            top_y += 64
                        # Doing 1 - (col_i%2) gets us same if odd column
                        top_x = (col_i + (1 - (col_i % 2))) % 32
                        self.tiles[top_y][top_x].propogated_densities[2] = density
                    elif i == 3:
                        # Bottom-right. One row below, one right (or same)
                        top_y = (row_i + 1) % 64
                        # Doing 1 - (col_i%2) gets us same if odd column
                        top_x = (col_i + (1 - (col_i % 2))) % 32
                        self.tiles[top_y][top_x].propogated_densities[3] = density
                    elif i == 4:
                        # Bottom. Two rows below.
                        top_y = (row_i + 2) % 64
                        self.tiles[top_y][col_i].propogated_densities[4] = density
                    elif i == 5:
                        # Bottom-left. One rows below.
                        top_y = (row_i + 1) % 64
                        # Doing  - (col_i%2) gets us same if even column
                        top_x = col_i - (col_i % 2)
                        self.tiles[top_y][top_x].propogated_densities[5] = density
                    elif i == 6:
                        # Top-left. One rows above.
                        top_y = (row_i - 1)
                        if top_y < 0:
                            top_y += 64
                        # Doing  - (col_i%2) gets us same if even column
                        top_x = col_i - (col_i % 2)
                        self.tiles[top_y][top_x].propogated_densities[6] = density


                

    def do_collision_step(self):
        for row in self.tiles:
            for hexagon in row:
                # Randomly assign densities.
                hexagon.densities = copy.copy(hexagon.propogated_densities)

                # As an experiment, let's use a collision operator
                # that sets the density in all directions to the average
                # density. I'm pretty sure this will *not* conserve energy
                # or momentum.
                average_density = sum(hexagon.densities) / len(hexagon.densities)
                hexagon.densities = [average_density for d in hexagon.densities]
                hexagon.recalculateDensity()


class HexafluidApp(App):
    def build(self):
        app = TileMap()
        Clock.schedule_interval(app.update, 1.0 / 60)
        return app

if __name__ == '__main__':
    HexafluidApp().run()
