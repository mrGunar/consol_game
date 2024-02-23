from enum import Enum


class Phrase(Enum):
    LOSE = "GAME OVER! YOU LOSE"
    WIN = "GAME OVER! You win"
    EXIT = "Press any key..."

    MONSTERS_REMAIN = "MONSTERS REMAINING"
