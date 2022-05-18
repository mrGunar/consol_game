from game import Game
from conf import Config
import os

if __name__ == "__main__":
    game = Game(count_monsters=Config.COUNT_MONSTER.value)
    os.system("cls")
    game.run()
