from conf import Config


class Player:
    def __init__(self, x=None, y=None) -> None:
        self._x = x
        self._y = y
        self.is_alive = True
        self.bullet = 0
        self.icon = Config.HUMAN_ICON.value
        self.last_direction = 'left'
    
    def step(self, x, y):
        self._x += x
        self._y += y

    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1

    def get_bullet(self, count):
        self.bullet += count

    def set_coord(self, x, y):
        self._x = x
        self._y = y

    @property
    def pos(self):
        return (self._x, self._y)
        
    
