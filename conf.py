from enum import Enum


class Config(Enum):

    MAP_HEIGHT = 5
    MAP_WIDTH = 5

    COUNT_MONSTER = 2

    BORDER_CELL = "\u25a1"
    EMPTY_CELL = "_"
    MONSTER_ICON = "M"
    HUMAN_ICON = "Y"
    ARMOUR_ICON = "W"