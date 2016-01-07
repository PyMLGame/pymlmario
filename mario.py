# coding: utf-8

from pymlgame.surface import Surface
from pymlgame.locals import RED, BLUE


class Mario:
    def __init__(self):
        self.normal = Surface(2, 4)
        self.normal.draw_line((0, 0), (1, 0), RED)
        self.normal.draw_dot((0, 1), (127, 0, 0))
        self.normal.draw_dot((1, 1), (255, 127, 0))
        self.normal.draw_dot((0, 2), RED)
        self.normal.draw_dot((1, 2), BLUE)
        self.normal.draw_line((0, 3), (1, 3), BLUE)

        self.current = self.normal

        self.x = 2.0
        self.y = 8.0
        self.width = self.current.width
        self.height = self.current.height

        self.direction = 1  # 0: left, 1: right

    def render(self):
        """
        Return current form of mario.

        :returns: Surface - Marios surface
        """
        return self.current
