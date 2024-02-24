from conf.map_config import MapConfig
from src.coordintate.coordinator import Coordinate


class Cell:
    obj: int
    coords: Coordinate
        


class Map:
    def __init__(self) -> None:
        self._fields = [
            ["_" for _ in range(MapConfig.MAP_HEIGHT.value)]
            for _ in range(MapConfig.MAP_WIDTH.value)
        ]
        self._monsters = None
        self._player = None
        self._objects = None
        self._fields = self.generate_map_board(self._fields)

    def generate_map_board(self, f):
        f[0] = f[-1] = [MapConfig.BORDER_CELL.value] * MapConfig.MAP_HEIGHT.value
        for el in f:
            el[0] = el[-1] = MapConfig.BORDER_CELL.value
        return f

    def show_map(self):
        for row in self._fields:
            print(*row)

    @property
    def fields(self):
        return self._fields

    def draw_map(self, objs):
        self._fields = [
            ["_" for _ in range(MapConfig.MAP_HEIGHT.value)]
            for _ in range(MapConfig.MAP_WIDTH.value)
        ]
        self._fields = self.generate_map_board(self._fields)

        for obj in objs:
            if obj.is_alive:
                self._fields[obj.x][obj.y] = obj.icon

    def add_monsters(self, monsters):
        self.monsters = monsters
    
    def set_icon(self, coords: Coordinate, icon) -> None:
        self.fields[coords.x][coords.y] = icon
