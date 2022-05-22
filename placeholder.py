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
    