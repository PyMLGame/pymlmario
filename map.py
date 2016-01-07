# coding: utf-8

from PIL import Image
from pymlgame.surface import Surface

NONBLOCKING = 0
BLOCKING = 1
DESTROYABLE = 2


class Map:
    def __init__(self, name):
        self.width = 0
        self.height = 0
        self._pixmap, self._nakedmap, self._colmap = self.load(name)

    def render_pixmap(self):
        """
        Renders the current view of of the map.

        :returns: Surface - The surface of the map
        """
        s = Surface(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                s.draw_dot((x, y), self._pixmap[x, y])
        return s

    def render_naked_map(self):
        """
        Renders the naked map without destroyable objects

        :returns: Surface - The surface of the naked map
        """
        s = Surface(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                s.draw_dot((x, y), self._nakedmap[x, y])
        return s

    def generate_collision_matrix(self):
        """
        Generates the collision matrix.

        :returns: list - 2-dimensional array of the collision map
        """
        def translate(color):
            if color == (0, 0, 0):
                return BLOCKING
            elif color == (127, 127, 127):
                return DESTROYABLE
            else:
                return NONBLOCKING

        colmat = {}
        for x in range(self.width):
            row = {}
            for y in range(self.height):
                row[y] = translate(self._colmap[x, y])
            colmat[x] = row

        return colmat

    def load(self, name):
        """
        Load map files.

        :param name: Base filename of map
        :type name: str
        :returns: tuple - pixel map and collision map
        """
        map_file = Image.open('maps/%s.png' % name)
        naked_file = Image.open('maps/%s_naked.png' % name)
        col_file = Image.open('maps/%s_collide.png' % name)

        self.width = map_file.size[0]
        self.height = map_file.size[1]

        map_data = map_file.load()
        naked_data = naked_file.load()
        col_data = col_file.load()

        if not (map_file.size == naked_file.size == col_file.size):
            print('Error: Sizes of map, naked and collide map differ!')
            return False

        return map_data, naked_data, col_data
