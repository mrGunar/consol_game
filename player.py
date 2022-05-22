from conf import Config
from enum import Enum
from placeholder import Object


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

    # def set_coord(self, x, y):
    #     self._x = x
    #     self._y = y

    # @property
    # def pos(self):
    #     return (self._x, self._y)
        
    
