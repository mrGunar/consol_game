from conf import Config


class Bullet:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.icon = Config.BULLET_CELL.value
