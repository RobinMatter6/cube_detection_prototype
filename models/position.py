from enum import Enum


class Position(Enum):
    STACKED = 1
    LEFT = 2
    RIGHT = 4
    FRONT = 8
    BACK = 16
    TOP = 32
    BOTTOM = 64
