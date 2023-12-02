from typing import Sequence

from models.color import Color


class Contour:

    def __init__(self, area: float, center: Sequence[int], color: Color):
        self.area = area
        self.center = center
        self.color = color

    def get_center_x(self):
        return self.center[0]

    def get_center_y(self):
        return self.center[1]

