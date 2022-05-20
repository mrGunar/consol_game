from conf import Config


class Monster:
    def __init__(self, x=None, y=None) -> None:
        self._x = x
        self._y = y
        self.is_alive = True
        self.icon = Config.MONSTER_ICON.value

    @classmethod
    def create_monster(cls):
        return Monster()

    def step(self, x, y):
        self._x += x
        self._y += y

    @property
    def pos(self):
        return (self._x, self._y)

    
    def kill(self):
        self.is_alive = False
        self.icon = Config.EMPTY_CELL.value
