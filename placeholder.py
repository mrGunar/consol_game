class Object:
    def __init__(self, x=None, y=None) -> None:
        self._x = x
        self._y = y

    def get_coords(self) -> tuple:
        return (self._x, self._y)

    def set_coords(self, x, y) -> None:
        self._x = x
        self._y = y

    