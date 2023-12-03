from enum import Enum


class Color(Enum):
    UNDEFINED = "undefined"
    NONE = ""
    BLUE = "blue"
    RED = "red"
    YELLOW = "yellow"

    def __str__(self):
        return self.value
