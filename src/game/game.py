import os
import random
import typing
import time

from src.map.map import Map
from src.coordintate.coordinator import Coordinate, generate_free_coord
from conf.map_config import MapConfig
from conf.phrases import Phrase
from src.objects.game_object import Player, Monster, Direction, Bullet, Grenade, BFG
from src.game.services import get_next_coord_for_monster, is_move_valid, find_monster_with_coord


class BiasCoords:
    LEFT = Coordinate(0, -1)
    RIGHT = Coordinate(0, 1)
    UP = Coordinate(-1, 0)
    DOWN = Coordinate(1, 0)


class PlayerCommands:
    def __init__(self, player, map):
        self.player = player
        self.map = map
        
    def move_up(self):
        bias = self.player.get_coords() + BiasCoords.UP
        if is_move_valid(bias, self.map):
            self.player.step(BiasCoords.UP)
            self.player.last_direction = Direction.UP
    
    def move_left(self):
        bias = self.player.get_coords() + BiasCoords.LEFT
        if is_move_valid(bias, self.map):
            self.player.step(BiasCoords.LEFT)
            self.player.last_direction = Direction.LEFT
    
    def move_down(self):
        bias = self.player.get_coords() + BiasCoords.DOWN
        if is_move_valid(bias, self.map):
            self.player.step(BiasCoords.DOWN)
            self.player.last_direction = Direction.DOWN

    def move_right(self):
        bias = self.player.get_coords() + BiasCoords.RIGHT
        if is_move_valid(bias, self.map):
            self.player.step(BiasCoords.RIGHT)
            self.player.last_direction = Direction.RIGHT
    
    def shoot_bullet(self):
        bullet = Bullet(self.player.get_coords())
        self.bullet_command = BulletCommand(bullet, self.map)
        self.bullet_command.bullet_fly(self.player.last_direction)


class BulletCommand:
    def __init__(self, bullet, _map):
        self.bullet = bullet
        self.map = _map
    
    def bullet_fly(self, direction: str) -> None:
        dx = 0
        dy = 0

        match direction:
            case Direction.UP:
                dx, dy = (1, 0)
            case Direction.DOWN:
                dx, dy = (-1, 0)
            case Direction.RIGHT:
                dx, dy = (0, -1)
            case Direction.LEFT:
                dx, dy = (0, 1)
        coords = Coordinate(-dx, -dy)
        
        while is_move_valid(self.bullet.get_coords(), self.map):
            self.bullet.set_coords(coords)
            kill_status = self.check_status_for_bullet_fly()
            self.map.set_icon(self.bullet.get_coords(), self.bullet.icon)
            if kill_status:
                break
            self.map.show_map()
            time.sleep(0.05)
            os.system("cls")

    def check_status_for_bullet_fly(self) -> bool:
        print(self.map.fields[self.bullet.x][self.bullet.y])
        if self.map.fields[self.bullet.x][self.bullet.y] == MapConfig.MONSTER_ICON.value:
            monster = find_monster_with_coord(self.bullet.x, self.bullet.y, self.map)
            if monster:
                print("HEADSHOT")
                time.sleep(1)
                monster.kill()
                return True
        return False


class Game:
    game = True

    def __init__(self, count_monsters=3) -> None:
        self.bussy_cells = list()
        self.map = Map()
        self.player = Player()
        self.player_commands = PlayerCommands(self.player, self.map)
        self.create_monsters(count_monsters)
        self.init()
    
    def create_monsters(self, count_monsters):
        self.monsters = [Monster.create_monster() for _ in range(count_monsters)]
        self.monsters = [x for x in self.monsters if x.is_alive]
        random.shuffle(self.monsters)
        self.map.add_monsters(self.monsters)

    def init(self):
        self.all_objects = [self.player] + self.monsters
        self.set_coords_to_obj(self.all_objects)       
        self.add_all_obj_to_map(self.all_objects)    

    def set_coords_to_obj(self, objs) -> None:
        for obj in objs:
            coords = generate_free_coord(self.bussy_cells)
            self.bussy_cells.append(coords)
            obj.set_coords(coords)

    def add_all_obj_to_map(self, objs) -> None:
        for obj in objs:
            self.map.set_icon(obj.get_coords(), obj.icon)

    def monsters_step(self) -> None:

        for x in self.monsters:
            old_cords = x.get_coords()
            self.bussy_cells.pop(self.bussy_cells.index(old_cords))

            new_cords = get_next_coord_for_monster(
                self.map, self.player, x.get_coords()
            )
            self.bussy_cells.append(new_cords)

            x.set_coords(new_cords)
            self.map.set_icon(new_cords, x.icon)

    def user_step(self, user_choice: str) -> None:
        match user_choice:
            case "w":
                self.player_commands.move_up()
            case "a":
                self.player_commands.move_left()
            case "s":
                self.player_commands.move_down()
            case "d":
                self.player_commands.move_right()
            case "z":
                self.player_commands.shoot_bullet()
            case "x":
                grenade = Grenade(self.player.get_coords())
                self.throw_grenade(grenade, self.player.last_direction)
            case "c":
                bfg = BFG(self.player.get_coords())
                self.bfg_shoot(bfg, self.player.last_direction)
            case _:
                print("Please repeat")
                return self.user_step(input("W A S D: "))
        self.map.set_icon(self.player.get_coords(), self.player.icon)


    def check_game_status(self) -> typing.Tuple[bool, bool]:
        available_monster = True if [x for x in self.monsters if x.is_alive] else False
        self.check_status_player_near_monsters()

        return available_monster, self.player.is_alive

    def check_status_player_near_monsters(self) -> None:
        nei = [(1, 1), (1, 0), (-1, 0), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]

        for i, j in nei:
            dx = self.player.x - i
            dy = self.player.y - j
            if (
                0 < dx < MapConfig.MAP_HEIGHT.value
                and 0 < dy < MapConfig.MAP_WIDTH.value
                and self.map.fields[dx][dy] == MapConfig.MONSTER_ICON.value
            ):
                self.player.kill_player()

    def throw_grenade(self, grenade, last_direction, d=3):
        match last_direction:
            case Direction.UP:
                dx, dy = (d, 0)
            case Direction.DOWN:
                dx, dy = (-d, 0)
            case Direction.RIGHT:
                dx, dy = (0, -d)
            case Direction.LEFT:
                dx, dy = (0, d)

        grenade.set_coords(Coordinate(-dx, -dy))

        self.explose_grenade(grenade)

    def explose_grenade(self, gren):
        nei = [
            (1, 1),
            (1, 0),
            (1, -1),
            (0, 1),
            (0, 0),
            (0, -1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]

        c = 0
        for i, j in nei:
            dx = gren.x - i
            dy = gren.y - j
            if is_move_valid(Coordinate(dx, dy), self.map):
                self.map.set_icon(Coordinate(dx, dy), gren.icon)
                monster = find_monster_with_coord(dx, dy, self.map)
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
                dd = (1, 0), (1, -1), (1, 1)
            case Direction.DOWN:
                dd = (-1, 0), (-1, -1), (-1, 1)
            case Direction.RIGHT:
                dd = (0, -1), (1, -1), (-1, -1)
            case Direction.LEFT:
                dd = (0, 1), (1, 1), (-1, 1)

        while (
            0 < bfg.x < MapConfig.MAP_HEIGHT.value - 1
            and 0 < bfg.y < MapConfig.MAP_WIDTH.value - 1
        ):
            for i, j in dd:
                dx = bfg.x - i
                dy = bfg.y - j
                if (
                    0 < dx < MapConfig.MAP_HEIGHT.value
                    and 0 < dy < MapConfig.MAP_WIDTH.value
                    and self.map.fields[dx][dy] != MapConfig.BORDER_CELL.value
                ):
                    self.map.set_icon(Coordinate(dx, dy), bfg.icon)
                    monster = find_monster_with_coord(dx, dy, self.map)
                    if monster:
                        monster.kill()

                    os.system("cls")
                    self.map.show_map()
                    time.sleep(0.05)
            bfg.set_coords(Coordinate(-dd[0][0], -dd[0][1]))

        time.sleep(1)

    def run(self) -> None:
        monster_status, player_status = True, True

        while Game.game:
            self.map.show_map()
            if not player_status:
                Game.game = False

                input(f"{Phrase.LOSE.value}\n{Phrase.EXIT.value}")
                break
            monsters_last = sum([1 for x in self.monsters if x.is_alive])
            print(f"{Phrase.MONSTERS_REMAIN.value}: {monsters_last}")

            user_choice = input("Your step: w a s d: ")
            self.user_step(user_choice)
            monster_status, player_status = self.check_game_status()
            if not monster_status:
                Game.game = False

                if player_status or not monster_status:
                    input(f"{Phrase.WIN.value}\n{Phrase.EXIT.value}")
                    exit()
                else:
                    input(f"{Phrase.LOSE.value}\n{Phrase.EXIT.value}")
                    exit()
                    
            self.monsters_step()
            self.add_all_obj_to_map(self.all_objects)

            self.map.draw_map(self.all_objects)

            os.system("cls")
