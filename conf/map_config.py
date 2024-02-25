from enum import Enum


class MapConfig(Enum):
    MAP_HEIGHT = 15
    MAP_WIDTH = 15

    COUNT_MONSTER = 3

    BULLET_CELL = "*"
    GRENADE_ICON = "+"
    BFG_CELL = "#"

    BORDER_CELL = "\u25a1"
    EMPTY_CELL = "_"
    MONSTER_ICON = "M"
    HUMAN_ICON = "Y"
    ARMOUR_ICON = "W"
