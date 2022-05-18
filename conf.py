from enum import Enum


class Config(Enum):

    MAP_HEIGHT = 40
    MAP_WIDTH = 40

    COUNT_MONSTER = 100

    BORDER_CELL = "\u25a1"
    EMPTY_CELL = "_"
    MONSTER_ICON = "M"
    HUMAN_ICON = "Y"
    ARMOUR_ICON = "W"