from conf.map_config import MapConfig


class Map:
    def __init__(self) -> None:
        self._field = [['_' for _ in range(MapConfig.MAP_HEIGHT.value)] for _ in range(MapConfig.MAP_WIDTH.value)]
        self._field = self.generate_map_board(self._field)
    
    def generate_map_board(self, f):
        f[0] = f[-1] = [MapConfig.BORDER_CELL.value] * MapConfig.MAP_HEIGHT.value
        for el in f:
            el[0] = el[-1] = MapConfig.BORDER_CELL.value
        return f

    def show_map(self):
        for row in self._field:
            print(*row)
    
    @property
    def fields(self):
        return self._field

    def draw_map(self, objs):
        self._field = [['_' for _ in range(MapConfig.MAP_HEIGHT.value)] for _ in range(MapConfig.MAP_WIDTH.value)]
        self._field = self.generate_map_board(self._field)

        for obj in objs:
            if obj.is_alive:
                self._field[obj._x][obj._y] = obj.icon 

    

    


