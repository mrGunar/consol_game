from enum import Enum


class Config(Enum):

    MAP_HEIGHT = 35
    MAP_WIDTH = 35

    COUNT_MONSTER = 3

    BULLET_CELL = '*'
    GRENADE_ICON = "+"
    BFG_CELL = "#"

    BORDER_CELL = "\u25a1"
    EMPTY_CELL = "_"
    MONSTER_ICON = "M"
    HUMAN_ICON = "Y"
    ARMOUR_ICON = "W"
    


class Phrase(Enum):

    LOSE = "GAME OVER! YOU LOSE"
    WIN = "GAME OVER! You win" 
    EXIT = "Press any key..."

    MONSTERS_REMAIN = "MONSTERS REMAINING"
