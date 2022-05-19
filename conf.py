from enum import Enum


class Config(Enum):

    MAP_HEIGHT = 4
    MAP_WIDTH = 4

    COUNT_MONSTER = 1

    BORDER_CELL = "\u25a1"
    EMPTY_CELL = "_"
    MONSTER_ICON = "M"
    HUMAN_ICON = "Y"
    ARMOUR_ICON = "W"