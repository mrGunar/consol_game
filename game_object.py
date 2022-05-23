from conf import Config
from enum import Enum


class Object:
    def __init__(self, x=None, y=None, is_alive=None, is_object=None) -> None:
        self._x = x
        self._y = y
        self._is_alive = is_alive
        self._is_object = is_object

    def get_coords(self) -> tuple:
        return (self._x, self._y)

    def set_coords(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def step(self, x: int, y: int) -> None:
        self._x += x
        self._y += y

    @property
    def is_alive(self):
        return self._is_alive


class Direction(Enum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'

class Player(Object):
    def __init__(self, x=None, y=None) -> None:
        super().__init__(is_alive=True, is_object=False)
        self.bullet = 0
        self.icon = Config.HUMAN_ICON.value
        self.last_direction = Direction.LEFT
    
    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1

    def get_bullet(self, count):
        self.bullet += count

        
    def kill_player(self) -> None:
        self._is_alive = False


class Monster(Object):
    def __init__(self, x=None, y=None) -> None:
        super().__init__(is_alive=True, is_object=False)
        self.icon = Config.MONSTER_ICON.value

    @classmethod
    def create_monster(cls):
        return Monster()

    def kill(self):
        self._is_alive = False
        self.icon = Config.EMPTY_CELL.value


class Bullet:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.icon = Config.BULLET_CELL.value


class Grenade:
    def __init__(self, x=None, y=None) -> None:
        self._x = x
        self._y = y

    def explose(self, x, y, objs):
        pass

