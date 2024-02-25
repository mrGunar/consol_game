import os
import time

from src.map.map import Map
from src.coordintate.coordinator import Coordinate
from conf.map_config import MapConfig
from src.games_types import Direction
from src.objects.weapons.bullet import Bullet
from src.objects.weapons.grenade import Grenade
from src.objects.weapons.bfg import BFG
from src.game.services import (
    get_next_coord_for_monster,
    is_move_valid,
    find_monster_with_coord,
)


class BiasCoords:
    LEFT = Coordinate(0, -1)
    RIGHT = Coordinate(0, 1)
    UP = Coordinate(-1, 0)
    DOWN = Coordinate(1, 0)


class CommonEngine:
    def __init__(self, _map: Map):
        self._map = _map


class PlayerCommands(CommonEngine):
    def __init__(self, obj, _map):
        super().__init__(_map)
        self.player = obj

    @property
    def player_coords(self):
        return self._map.map_actions.get_obj_coords(self.player)

    def move_up(self):
        player_coords = self.player_coords
        new_coords = player_coords + BiasCoords.UP

        if is_move_valid(new_coords, self._map):
            self._map.map_actions.move_object(self.player, player_coords, new_coords)
            self.player.last_direction = Direction.UP

    def move_left(self):
        player_coords = self.player_coords
        new_coords = player_coords + BiasCoords.LEFT

        if is_move_valid(new_coords, self._map):
            self._map.map_actions.move_object(self.player, player_coords, new_coords)
            self.player.last_direction = Direction.LEFT

    def move_down(self):
        player_coords = self.player_coords
        new_coords = player_coords + BiasCoords.DOWN

        if is_move_valid(new_coords, self._map):
            self._map.map_actions.move_object(self.player, player_coords, new_coords)
            self.player.last_direction = Direction.DOWN

    def move_right(self):
        player_coords = self.player_coords
        new_coords = player_coords + BiasCoords.RIGHT

        if is_move_valid(new_coords, self._map):
            self._map.map_actions.move_object(self.player, player_coords, new_coords)
            self.player.last_direction = Direction.RIGHT

    def user_step(self, user_choice: str) -> None:
        match user_choice:
            case "w":
                self.move_up()
            case "a":
                self.move_left()
            case "s":
                self.move_down()
            case "d":
                self.move_right()
            case "z":
                self.shoot_bullet()
            case "x":
                grenade = Grenade(self.player.get_coords())
                self.throw_grenade(grenade, self.player.last_direction)
            case "c":
                bfg = BFG(self.player.get_coords())
                self.bfg_shoot(bfg, self.player.last_direction)
            case "q":
                exit()
            case _:
                print("Please repeat")
                return self.user_step(input("W A S D: "))

    def shoot_bullet(self):
        bullet = Bullet(self.player.get_coords())
        self.bullet_command = BulletCommand(bullet, self._map)
        self.bullet_command.bullet_fly(self.player.last_direction)


class MonsterCommands(CommonEngine):
    def __init__(self, _map):
        super().__init__(_map)

    def monster_coords(self, monster):
        return self._map.map_actions.get_obj_coords(monster)

    def monster_step(self, monster, player_coords):
        monster_coords = self.monster_coords(monster)
        new_monster_cords = get_next_coord_for_monster(
            self._map,
            self._map.map_actions.get_obj_coords(player_coords),
            self._map.map_actions.get_obj_coords(monster),
        )

        self._map.map_actions.move_object(monster, monster_coords, new_monster_cords)


class BulletCommand:
    def __init__(self, bullet, _map):
        self.bullet = bullet
        self.map = _map

    def bullet_fly(self, direction: str) -> None:
        match direction:
            case Direction.UP:
                coords = BiasCoords.UP
            case Direction.DOWN:
                coords = BiasCoords.DOWN
            case Direction.RIGHT:
                coords = BiasCoords.RIGHT
            case Direction.LEFT:
                coords = BiasCoords.LEFT

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
        if (
            self.map.fields[self.bullet.x][self.bullet.y]
            == MapConfig.MONSTER_ICON.value
        ):
            monster = find_monster_with_coord(
                self.bullet.get_coords(), self.map.monsters
            )
            if monster:
                print("~~HEADSHOT~~")
                time.sleep(1)
                monster.kill()
                return True
        return False
