import os
import random
import typing
import time

from src.map.map import Map
from src.coordintate.coordinator import Coord, Coordinate
from conf.map_config import MapConfig
from conf.phrases import Phrase
from src.objects.game_object import Player, Monster, Direction, Bullet, Grenade, BFG
from src.game.services import get_next_coord_for_monster


class Game:

    game = True

    def __init__(self, count_monsters=3) -> None:
        self.bussy_cells = list()
        self.map = Map()
        self.player = Player()
        self.monsters = [Monster.create_monster() for _ in range(count_monsters)]
        self.monsters = [x for x in self.monsters if x.is_alive]
        self.all_objects = [self.player] + self.monsters
        self.set_coords_to_obj(self.all_objects)

    def set_coords_to_obj(self, objs) -> None:
        for obj in objs:
            coords = Coord.generate_free_coord(self.bussy_cells)
            self.bussy_cells.append(coords)
            obj.set_coords(coords)

    def set_icon(self, coords: Coordinate, icon) -> None:
        self.map.fields[coords.x][coords.y] = icon

    def add_all_obj_to_map(self, objs) -> None:
        for obj in objs:
            self.set_icon(obj.get_coords(), obj.icon)

    def monsters_step(self) -> None:

        random.shuffle(self.monsters)

        for x in self.monsters:
            old_cords = x.get_coords()
            self.bussy_cells.pop(self.bussy_cells.index(old_cords))

            new_cords = get_next_coord_for_monster(self.map, self.player, x.get_coords())
            self.bussy_cells.append(new_cords)

            x.set_coords(new_cords)
            self.set_icon(new_cords, x.icon)

    def user_step(self, user_choice: str) -> None:
        match user_choice:
            case "w":
                self.player.step(-1,0)
                self.player.last_direction = Direction.UP
            case "a":
                self.player.step(0,-1)
                self.player.last_direction = Direction.LEFT
            case "s":
                self.player.step(1,0)
                self.player.last_direction = Direction.DOWN
            case "d":
                self.player.step(0,1)
                self.player.last_direction = Direction.RIGHT
            case "z":
                bullet = Bullet(self.player.get_coords())
                self.bullet_fly(bullet, self.player.last_direction)
            case "x":
                grenade = Grenade(self.player.get_coords())
                self.throw_grenade(grenade, self.player.last_direction)
            case "c":
                bfg = BFG(self.player.get_coords())
                self.bfg_shoot(bfg, self.player.last_direction)
            case _:
                print("Please repeat")
                return self.user_step(input("W A S D: "))
        self.set_icon(self.player.get_coords(), self.player.icon)


    def bullet_fly(self, bullet, last_direction: str) -> None:
        dx = 0
        dy = 0

        match last_direction:
            case Direction.UP:
                dx, dy = (1,0)
            case Direction.DOWN:
                dx, dy = (-1, 0)
            case Direction.RIGHT:
                dx, dy = (0,-1)
            case Direction.LEFT:
                dx, dy = (0,1)

        while 0 < bullet.x < MapConfig.MAP_HEIGHT.value-1 and 0 < bullet.y < MapConfig.MAP_WIDTH.value-1:
            bullet.change_coords(-dx, -dy)
            kill_status = self.check_status_for_bullet_fly(bullet)
            self.set_icon(bullet.get_coords(), bullet.icon)
            if kill_status:
                break
            self.map.show_map()
            time.sleep(0.05)
            os.system("cls")

    def check_status_for_bullet_fly(self, bullet) -> bool:
        print(self.map.fields[bullet.x][bullet.y])
        if self.map.fields[bullet.x][bullet.y] == MapConfig.MONSTER_ICON.value:
            monster = self.find_monster_with_coord(bullet.x, bullet.y)
            if monster:
                print("HEADSHOT")
                time.sleep(1)
                monster.kill()
                return True
        return False

    def find_monster_with_coord(self, x: int, y: int) -> object:
        for m in self.monsters:
            if (x, y) == (m.x, m.y):
                return m

    def check_game_status(self) -> typing.Tuple[bool, bool]:
        available_monster = True if [x for x in self.monsters if x.is_alive] else False
        self.check_status_player_near_monsters()

        return available_monster, self.player.is_alive

    def check_status_player_near_monsters(self) -> None:
        nei = [(1,1), (1,0), (-1,0), (-1,1), (-1,0), (-1,-1), (0, 1), (0, -1)]

        for i, j in nei:
            dx = self.player.x - i
            dy = self.player.y - j
            if 0 < dx < MapConfig.MAP_HEIGHT.value and 0 < dy < MapConfig.MAP_WIDTH.value and \
            self.map.fields[dx][dy] == MapConfig.MONSTER_ICON.value:
                self.player.kill_player()

    def throw_grenade(self,grenade, last_direction, d=3):

        match last_direction:
            case Direction.UP:
                dx, dy = (d,0)
            case Direction.DOWN:
                dx, dy = (-d, 0)
            case Direction.RIGHT:
                dx, dy = (0,-d)
            case Direction.LEFT:
                dx, dy = (0,d)

        grenade.change_coords(-dx, -dy)

        self.explose_grenade(grenade)

    def explose_grenade(self, gren):
        nei = [(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1, 1), (-1,0), (-1,-1)]

        c = 0
        for i, j in nei:
            dx = gren.x - i
            dy = gren.y - j
            if 0 < dx < MapConfig.MAP_HEIGHT.value and 0 < dy < MapConfig.MAP_WIDTH.value and \
                self.map.fields[dx][dy] != MapConfig.BORDER_CELL.value:
                self.set_icon(Coordinate(dx, dy), gren.icon)
                monster = self.find_monster_with_coord(dx, dy)
                if monster:
                    monster.kill()
                    c += 1
                os.system("cls")
                self.map.show_map()
                time.sleep(0.2)

        print(f"YOU KILL {c} MONSTERS")
        time.sleep(1)


    def bfg_shoot(self, bfg, last_direction):
        match last_direction:
            case Direction.UP:
                dd = (1,0), (1,-1), (1,1)
            case Direction.DOWN:
                dd = (-1,0), (-1,-1), (-1,1)
            case Direction.RIGHT:
                dd = (0,-1), (1,-1), (-1,-1)
            case Direction.LEFT:
                dd = (0,1), (1,1), (-1,1)


        
        while 0 < bfg.x < MapConfig.MAP_HEIGHT.value-1 and 0 < bfg.y < MapConfig.MAP_WIDTH.value-1:
            for i, j in dd:
                dx = bfg.x - i
                dy = bfg.y - j
                if 0 < dx < MapConfig.MAP_HEIGHT.value and 0 < dy < MapConfig.MAP_WIDTH.value and \
                    self.map.fields[dx][dy] != MapConfig.BORDER_CELL.value:
                    self.set_icon(Coordinate(dx, dy), bfg.icon)
                    monster = self.find_monster_with_coord(dx, dy)
                    if monster:
                        monster.kill()
                        
                    os.system("cls")
                    self.map.show_map()
                    time.sleep(0.05)
            bfg.change_coords(-dd[0][0], -dd[0][1])

        time.sleep(1)

                
    def run(self) -> None:
        self.add_all_obj_to_map(self.all_objects)
        monster_status, player_status = True, True
        while Game.game:
            self.map.show_map()
            if not player_status:
                Game.game = False

                input(f"{Phrase.LOSE.value}\n{Phrase.EXIT.value}")
                break 
            monsters_last = sum([1 for x in self.monsters if x.is_alive])
            print(f'{Phrase.MONSTERS_REMAIN.value}: {monsters_last}')

            user_choice = input("Your step: w a s d: ")
            self.user_step(user_choice)
            monster_status, player_status = self.check_game_status()
            if not monster_status:
                Game.game = False

                if player_status or not monster_status:
                    input(f"{Phrase.WIN.value}\n{Phrase.EXIT.value}")
                else:
                    input(f"{Phrase.LOSE.value}\n{Phrase.EXIT.value}")
                
            self.monsters_step()
            self.add_all_obj_to_map(self.all_objects)

            self.map.draw_map(self.all_objects)

            os.system("cls")
