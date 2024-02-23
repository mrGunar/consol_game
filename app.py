import os
import argparse

from src.game.game import Game
from conf.map_config import MapConfig


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--monsters", help="number of monsters in game",
                    type=int, default=MapConfig.COUNT_MONSTER.value)
    args = parser.parse_args()


    game = Game(count_monsters=args.monsters)
    os.system("cls")
    game.run()
