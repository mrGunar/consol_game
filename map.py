import imp
from conf import Config

class Map:
    def __init__(self) -> None:
        self.field = [['_' for _ in range(Config.MAP_HEIGHT.value)] for _ in range(Config.MAP_WIDTH.value)]
        self.field = self.generate_map_board(self.field)
    
    def generate_map_board(self, f):
        f[0] = f[-1] = [Config.BORDER_CELL.value] *Config.MAP_HEIGHT.value
        for el in f:
            el[0] = el[-1] = Config.BORDER_CELL.value
        return f

    def show_map(self):
        for row in self.field:
            print(*row)
    
    @property
    def fields(self):
        return self.field

    def draw_map(self, objs):
        self.field = [['_' for _ in range(Config.MAP_HEIGHT.value)] for _ in range(Config.MAP_WIDTH.value)]
        self.field = self.generate_map_board(self.field)

        for obj in objs:
            self.field[obj._x][obj._y] = obj.icon 

    

    


