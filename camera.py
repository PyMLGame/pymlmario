# coding: utf-8


class Camera:
    def __init__(self, map_width, map_height, width=40, height=16, position=(0, 0), dz_width=12, dz_height=6):
        self.width = width
        self.height = height
        self._map_width = map_width
        self._map_height = map_height
        self.x = 0
        self.y = 0

        self._deadzone_width = dz_width
        self._deadzone_height = dz_height
        self._deadzone_x = 0
        self._deadzone_y = 0
        self.update_deadzone()

        self.update(position)

    def check_camera_boundaries(self):
        self.x = max(self.x, 0)  # fix left border
        self.x = min(self.x, self._map_width - self.width)  # fix right border
        self.y = max(self.y, 0)  # fix bottom border
        self.y = min(self.y, self._map_height - self.height)  # fix top border

    def update_deadzone(self):
        self._deadzone_x = self.x + (self.width - self._deadzone_width) / 2
        self._deadzone_y = self.y + (self.height - self._deadzone_height) / 2

    def update(self, position):
        # check deadzone
        changed = False
        if position[0] < self._deadzone_x:
            self.x = self.x - (self._deadzone_x - position[0])
            changed = True
        elif position[0] > self._deadzone_x + self._deadzone_width:
            self.x += position[0] - self._deadzone_x - self._deadzone_width
            changed = True

        if position[1] < self._deadzone_y:
            self.y -= (self._deadzone_y - position[1])
            changed = True
        elif position[1] > self._deadzone_y + self._deadzone_height:
            self.y = self.y + (position[1] - self._deadzone_y - self._deadzone_height)
            changed = True

        if changed:
            self.check_camera_boundaries()
            self.update_deadzone()
