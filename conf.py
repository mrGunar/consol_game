from enum import Enum


class Config(Enum):

    MAP_HEIGHT = 20
    MAP_WIDTH = 20

    COUNT_MONSTER = 2

    BULLET_CELL = '*'

    BORDER_CELL = "\u25a1"
    EMPTY_CELL = "_"
    MONSTER_ICON = "M"
    HUMAN_ICON = "Y"
    ARMOUR_ICON = "W"