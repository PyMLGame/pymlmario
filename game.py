#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

import pymlgame
from pymlgame.locals import *
from pymlgame.screen import Screen
from pymlgame.clock import Clock
from pymlgame.surface import Surface

from map import Map, BLOCKING, DESTROYABLE, NONBLOCKING
from mario import Mario
from camera import Camera

MATELIGHT_WIDTH = 40
MATELIGHT_HEIGHT = 16

LEFT = 0
RIGHT = 1
JUMP = 2


class Game:
    def __init__(self):
        pymlgame.init()

        self.screen = Screen()
        # self.screen = Screen(host='matelight')
        self.clock = Clock(5)

        self.map = Map('1-1')
        self.mario = Mario()

        self.world = self.map.render_pixmap()
        self.colmat = self.map.generate_collision_matrix()

        for y in range(self.map.height):
            print('%02d %02d ' % (y, self.convert_y(y)), end='')
            for x in range(self.map.width):
                print(self.colmat[x][y], end='')
            print()

        self.gameover = False

        self.camera = Camera(self.map.width, self.map.height)

    def collide(self, x, y):
        """
        Check for a collision on the given position.

        :param x: x coord to check for collision
        :type x: int
        :param y: y coord to check for collision
        :type y: int
        :returns: bool - Collision detected?
        """
        return self.colmat[int(x)][self.convert_y(int(y))]

    def convert_y(self, y):
        """
        Converts coords from bottom 0 to top 0 for drawing.

        :param y: y coord with 0 at the bottom
        :type y: int
        :returns: int - y coord with 0 at the top
        """
        return self.map.height - y - 1

    def update(self):
        vel_x = 0
        vel_y = 0
        # apply jump force
        vel_y + self.mario.jumping
        if self.mario.jumping == 2:
            self.mario.jumping = 1
        elif self.mario.jumping == 1:
            self.mario.jumping = 0
        # apply movement force
        vel_x + self.mario.moving
        # apply gravity/falling
        vel_y -= 1
        # Compute resulting velocity
        # Apply resulting velocity and update position
        new_x = self.mario.x + vel_x
        new_y = self.mario.y + vel_y
        print('X: %d -> %d' % (self.mario.x, new_x))
        print('Y: %d -> %d' % (self.mario.y, new_y))
        print('C: %d' % self.colmat[new_x][self.convert_y(new_y)])
        print('R: %d' % self.collide(new_x, self.convert_y(new_y)))
        # Check collisions between objects
        # If collision, resolve it by moving back
        old_y = self.mario.y
        if not self.collide(self.mario.x, new_y) > 0:
            self.mario.y = new_y
        if not self.collide(new_x, old_y) > 0:
            self.mario.x = new_x

        # out of map?
        if self.mario.y < 0 or self.mario.x + self.mario.width <= 0 or self.mario.x >= self.map.width:
            self.gameover = True

        # camera
        self.camera.update((self.mario.x, self.mario.y))

        # autowalk
        # self.mario.x += 1

    def render(self):
        self.screen.reset()

        self.screen.blit(self.world, (int(0 - self.camera.x),
                                      int(0 - (self.convert_y(self.camera.y) - self.camera.height))))
        self.screen.blit(self.mario.current, (int(self.mario.x - self.camera.x),
                                              int(self.convert_y(self.mario.y + self.mario.height) - (self.convert_y(self.camera.y) - self.camera.height))))

        self.screen.update()
        self.clock.tick()

    def handle_events(self):
        for event in pymlgame.get_events():
            if event.type == E_PING:
                print(datetime.now(), '# ping from', event.uid)
            else:
                print(datetime.now(), '# unknown event', event.uid, event.type)

    def start(self):
        try:
            while not self.gameover:
                self.handle_events()
                self.update()
                self.render()
                if self.gameover:
                    break
            print('game over!')
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    g = Game()
    g.start()
