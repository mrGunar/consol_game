from conf import Config


class AliveObject:
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
        # import pdb;pdb.set_trace()
        if 0 < self._x+x < Config.MAP_HEIGHT.value-1 and 0 < self._y+y < Config.MAP_WIDTH.value-1:
            self._x += x
            self._y += y

    @property
    def is_alive(self):
        return self._is_alive


class WeaponObject:
    def __init__(self, x=None, y=None):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def change_coords(self, new_x, new_y):
        self._x = new_x
        self._y = new_y