from ssl import OP_ENABLE_MIDDLEBOX_COMPAT
from map import Map
from player import Player
from monster import Monster
from coordinator import Coord
import itertools
from conf import Config
import random

import os

class Game:

    game = True

    def __init__(self, count_monsters=3) -> None:
        self.bussy_cells = list()
        self.map = Map()
        self.player = Player()
        self.monsters = [Monster.create_monster() for _ in range(count_monsters)]
        self.all_objects = [self.player] + self.monsters
        self.set_coords_to_obj(self.all_objects)

    def set_coords_to_obj(self, objs):
        for obj in objs:
            coords = Coord.generate_free_coord(self.bussy_cells)
            self.bussy_cells.append(coords)
            obj._x, obj._y = coords

    def get_available_cord(self, x, y):
        nei = [(1,1), (1,0), (-1,0), (-1,1), (-1,0), (-1,-1), (0, 1), (0, -1)]

        res = []
        for i, j in nei:
            dx = x - i
            dy = y - j
            if 0 < dx < Config.MAP_HEIGHT.value and 0 < dy < Config.MAP_WIDTH.value and \
            self.map.field[dx][dy] == Config.EMPTY_CELL.value:
                res.append((dx, dy))

        return random.choice(res) if res else (x, y)

    def set_coord(self, obj, x, y):
        obj._x = x
        obj._y = y

    def set_icon(self, x, y, icon):
        self.map.field[x][y] = icon

    def add_all_obj_to_map(self, objs):
        for obj in objs:
            self.set_icon(obj._x, obj._y, obj.icon)

    def monsters_step(self):
        available_monster = [x for x in self.monsters if x.is_alive]

        random.shuffle(available_monster)
        for x in available_monster:
            old_cords = (x._x, x._y)
            self.bussy_cells.pop(self.bussy_cells.index(old_cords))

            new_cords = self.get_available_cord(*x.pos)
            self.bussy_cells.append(new_cords)
            
            self.set_coord(x, *new_cords)
            self.set_icon(*new_cords, x.icon)

    def user_step(self, user_choice):
        match user_choice:
            case "w":
                self.player.step(-1,0)
                self.player.last_direction = "up"
            case "a":
                self.player.step(0,-1)
                self.player.last_direction = "left"
            case "s":
                self.player.step(1,0)
                self.player.last_direction = "down"
            case "d":
                self.player.step(0,1)
                self.player.last_direction = "right"
            case "z":
                pass
            case _:
                print("Please repeat")
                return self.user_step(input("W A S D: "))
        self.set_icon(self.player._x, self.player._y, self.player.icon)

    def run(self):
        self.add_all_obj_to_map(self.all_objects)
        self.map.show_map()
        while Game.game:
            
            
            self.monsters_step()
            self.add_all_obj_to_map(self.all_objects)
            self.map.draw_map(self.all_objects)
            self.map.show_map()
            # import pdb;pdb.set_trace()
            import time;time.sleep(1)




            user_choice = input("Your step: w a s d: ")
            self.user_step(user_choice)
            os.system("cls")

        