from enum import Enum

from conf.map_config import MapConfig
from src.objects.objects import AliveObject, WeaponObject
from src.coordintate.coordinator import Coordinate


class Direction(Enum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'


class Player(AliveObject):
    def __init__(self, coords: Coordinate = Coordinate(None, None)) -> None:
        super().__init__(is_alive=True, is_object=False)
        self.bullet = 0
        self.icon = MapConfig.HUMAN_ICON.value
        self.last_direction = Direction.LEFT
    
    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1

    def get_bullet(self, count):
        self.bullet += count

        
    def kill_player(self) -> None:
        self._is_alive = False


class Monster(AliveObject):
    def __init__(self, coords: Coordinate = Coordinate(None, None)) -> None:
        super().__init__(is_alive=True, is_object=False)
        self.icon = MapConfig.MONSTER_ICON.value

    @classmethod
    def create_monster(cls):
        return Monster()

    def kill(self):
        self._is_alive = False
        self.icon = MapConfig.EMPTY_CELL.value



class Bullet(WeaponObject):
    def __init__(self, coords: Coordinate):
        super().__init__(coords)
        self.icon = MapConfig.BULLET_CELL.value


class Grenade(WeaponObject):
    def __init__(self, coords: Coordinate) -> None:
        super().__init__(coords)
        self.icon = MapConfig.GRENADE_ICON.value

    def explose(self, coords, objs):
        pass


class BFG(WeaponObject):
    def __init__(self, coords: Coordinate) -> None:
        super().__init__(coords)
        self.icon = MapConfig.BFG_CELL.value
