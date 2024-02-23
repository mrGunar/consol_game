from src.objects.object import Object
from src.coordintate.coordinator import Coordinate


class AliveObject(Object):
    def __init__(
        self, coords: Coordinate = Coordinate(None, None), is_alive=None, is_object=None
    ) -> None:
        super().__init__(coords)
        self._is_alive = is_alive
        self._is_object = is_object

    def set_coords(self, coords: Coordinate) -> None:
        self._coordinates = coords

    def step(self, bias: Coordinate) -> None:
        self._coordinates = Coordinate(
            self._coordinates.x + bias.x, self._coordinates.y + bias.y
        )

    @property
    def is_alive(self):
        return self._is_alive
