from conf.map_config import MapConfig
from src.coordintate.coordinator import Coordinate
from src.objects.map_objects import EmptyCell, Border


class FieldsCreator:
    def create_fields(self, with_board: bool = True) -> dict:
        self._fields = {
            Coordinate(i, j): EmptyCell()
            for i in range(MapConfig.MAP_HEIGHT.value)
            for j in range(MapConfig.MAP_WIDTH.value)
        }
        if with_board:
            self.generate_board()

        return self._fields

    def generate_board(self) -> None:
        for i in range(MapConfig.MAP_HEIGHT.value):
            self._fields[Coordinate(i, 0)] = Border()
            self._fields[Coordinate(0, i)] = Border()
            self._fields[Coordinate(MapConfig.MAP_HEIGHT.value - 1, i)] = Border()
            self._fields[Coordinate(i, MapConfig.MAP_WIDTH.value - 1)] = Border()
