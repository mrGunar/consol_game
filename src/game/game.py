import os
import typing
import time

from src.map.map import Map
from src.coordintate.coordinator import Coordinate
from conf.map_config import MapConfig
from conf.phrases import Phrase
from src.objects.monster import Monster
from src.objects.player import Player
from src.game.services import (
    is_move_valid,
    find_monster_with_coord,
)
from src.game.engine import PlayerCommands, MonsterCommands
from src.games_types import Direction


class Game:
    game = True

    def __init__(self, count_monsters=3) -> None:
        self.player = Player()
        self.monsters = [Monster.create_monster() for _ in range(count_monsters)]
        self.objects = []

        self.map = (
            Map().add_fields().add_monsters(self.monsters).add_player(self.player)
        )
        self.init_objects_on_map(self.map)
        self.player_commands = PlayerCommands(self.player, self.map)
        self.monster_commands = MonsterCommands(self.map)

    def init_objects_on_map(self, map):
        free_coords = map.map_actions.get_empty_cells_coords()
        import random

        random.shuffle(free_coords)
        for monster in self.map._monsters:
            coord = free_coords.pop()
            self.map.fields[coord] = monster

        coord = free_coords.pop()
        map.fields[coord] = self.map._player

        for obj in self.objects:
            coord = free_coords.pop()
            map.fields[coord] = obj

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
            self.map.map_actions.show_map()
            if not player_status:
                Game.game = False

                input(f"{Phrase.LOSE.value}\n{Phrase.EXIT.value}")
                break

            user_choice = input("Your step: w a s d: ")
            self.player_commands.user_step(user_choice)
            self.map.map_actions.show_map()
            os.system("cls")

            for m in self.monsters:
                self.monster_commands.monster_step(m, self.player)
            continue

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
