from src.coordintate.coordinator import Coordinate


class Object:
    def __init__(self, coordinates: Coordinate):
        self._coordinates = coordinates
    
    def get_coords(self) -> Coordinate:
        return self._coordinates

    def set_coords(self, coords: Coordinate) -> None:
        self._coordinates = Coordinate(coords.x + self.x, coords.y + self.y)

    @property
    def x(self):
        return self._coordinates.x

    @property
    def y(self):
        return self._coordinates.y
