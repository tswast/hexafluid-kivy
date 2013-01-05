import kivy
kivy.require('1.5.1')

# here, activate monitor module for FPS
# from kivy.config import Config
# Config.set('modules', 'monitor', '')

from random import random
from math import sqrt
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty


class Hexagon(Widget):
    tileradius = NumericProperty(1.0)
    density = NumericProperty(1.0)
    density_top_left = NumericProperty(1.0)
    density_top_middle = NumericProperty(1.0)
    density_top_right = NumericProperty(1.0)
    density_bottom_left = NumericProperty(1.0)
    density_bottom_middle = NumericProperty(1.0)
    density_bottom_right = NumericProperty(1.0)
    density_center = NumericProperty(1.0)

    def recalculateDensity(self):
        self.density = (self.density_top_left +
                self.density_top_middle +
                self.density_top_right +
                self.density_bottom_left +
                self.density_bottom_middle +
                self.density_bottom_right +
                self.density_center) / 7.0


class TileMap(RelativeLayout):
    def __init__(self, **kwargs):
        super(TileMap, self).__init__(**kwargs) # init ScatterPlane with above parameters

        # How many tiles to make? 32x64?
        tileradius = 8
        self.tiles = []
        for y_tile in xrange(64):
            row = []
            self.tiles.append(row)
            for x_tile in xrange(32):
                hexagon = Hexagon(
                    pos=((x_tile+1) * 3 * tileradius + (y_tile % 2) * (1.5 * tileradius),
                        (y_tile+1) * 0.5 * sqrt(3) * tileradius),
                    size_hint=(1.0/64, 1.0/64))
                self.add_widget(hexagon)
                hexagon.tileradius = tileradius
                hexagon.height=(tileradius*sqrt(3))

                # Randomly assign densities.
                hexagon.density_top_left = random()
                hexagon.density_top_middle = random()
                hexagon.density_top_right = random()
                hexagon.density_bottom_left = random()
                hexagon.density_bottom_middle = random()
                hexagon.density_bottom_right = random()
                hexagon.density_center = random()
                hexagon.recalculateDensity()
                row.append(hexagon)

    def update(self, *args, **kwargs):
        self.do_propagation_step()
        self.do_collision_step()

    def do_propagation_step(self):
        pass

    def do_collision_step(self):
        for row in self.tiles:
            for hexagon in row:
                # Randomly assign densities.
                hexagon.density_top_left = random()
                hexagon.density_top_middle = random()
                hexagon.density_top_right = random()
                hexagon.density_bottom_left = random()
                hexagon.density_bottom_middle = random()
                hexagon.density_bottom_right = random()
                hexagon.density_center = random()
                hexagon.recalculateDensity()


class HexafluidApp(App):
    def build(self):
        app = TileMap()
        Clock.schedule_interval(app.update, 0.5)
        return app

if __name__ == '__main__':
    HexafluidApp().run()
