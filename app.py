from game import Game
from conf import Config
import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--monsters", help="number of monsters in game",
                    type=int, default=Config.COUNT_MONSTER.value)
    args = parser.parse_args()


    game = Game(count_monsters=args.monsters)
    os.system("cls")
    game.run()
