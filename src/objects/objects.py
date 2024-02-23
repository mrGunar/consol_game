from conf.map_config import MapConfig
from src.coordintate.coordinator import Coordinate


class AliveObject:
    def __init__(self, coords: Coordinate = Coordinate(None, None), is_alive=None, is_object=None) -> None:
        self._coordinates = coords
        self._is_alive = is_alive
        self._is_object = is_object

    def get_coords(self) -> Coordinate:
        return self._coordinates 

    def set_coords(self, coords: Coordinate) -> None:
        self._coordinates = coords

    def step(self, x: int, y: int) -> None:
        if 0 < self.x + x < MapConfig.MAP_HEIGHT.value - 1 and 0 < self.y + y < MapConfig.MAP_WIDTH.value - 1:
            self._coordinates = Coordinate(self._coordinates.x + x, self._coordinates.y + y)

    @property
    def is_alive(self):
        return self._is_alive
    
    @property
    def x(self):
        return self._coordinates.x

    @property
    def y(self):
        return self._coordinates.y


class WeaponObject:
    def __init__(self, coords: Coordinate = Coordinate(None, None)):
        self._coordinates = coords

    @property
    def x(self):
        return self._coordinates.x

    @property
    def y(self):
        return self._coordinates.y
    
    def get_coords(self) -> Coordinate:
        return self._coordinates 
    

    def change_coords(self, new_x, new_y):
        self._coordinates = Coordinate(self._coordinates.x + new_x, self._coordinates.y + new_y)
