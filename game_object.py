from conf import Config
from enum import Enum
from objects import AliveObject, WeaponObject


class Direction(Enum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'


class Player(AliveObject):
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


class Monster(AliveObject):
    def __init__(self, x=None, y=None) -> None:
        super().__init__(is_alive=True, is_object=False)
        self.icon = Config.MONSTER_ICON.value

    @classmethod
    def create_monster(cls):
        return Monster()

    def kill(self):
        self._is_alive = False
        self.icon = Config.EMPTY_CELL.value



class Bullet(WeaponObject):
    def __init__(self, x=None, y=None):
        super().__init__(x, y)
        self.icon = Config.BULLET_CELL.value


class Grenade(WeaponObject):
    def __init__(self, x=None, y=None) -> None:
        super().__init__(x, y)
        self.icon = Config.GRENADE_ICON.value

    def explose(self, x, y, objs):
        pass


class BFG(WeaponObject):
    def __init__(self, x=None, y=None) -> None:
        super().__init__(x, y)
        self.icon = Config.BFG_CELL.value
