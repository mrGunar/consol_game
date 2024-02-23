import random
from dataclasses import dataclass

from conf.map_config import MapConfig


@dataclass
class Coordinate:
    x: int | None
    y: int | None



class Coord:
    @staticmethod
    def check_coord(coord, check_list: list) -> bool:
        return coord in check_list

    @staticmethod
    def generate_free_coord(check_list: list) -> Coordinate:
        """Generate free coordinates"""
        while 1:
            x = random.randint(1, MapConfig.MAP_HEIGHT.value - 2) 
            y = random.randint(1, MapConfig.MAP_WIDTH.value - 2)
            if (x, y) not in check_list:
                return Coordinate(x, y)
