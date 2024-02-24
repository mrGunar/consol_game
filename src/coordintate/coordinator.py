import random
from dataclasses import dataclass

from conf.map_config import MapConfig


@dataclass
class Coordinate:
    x: int | None
    y: int | None

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other: "Coordinate") -> bool:
        return self.x == other.x and self.y == other.y

def check_coord(coord: Coordinate, check_list: list[Coordinate]) -> bool:
    return coord in check_list


def generate_free_coord(check_list: list[Coordinate]) -> Coordinate:
    """Generate free coordinates."""
    while 1:
        x = random.randint(1, MapConfig.MAP_HEIGHT.value - 2)
        y = random.randint(1, MapConfig.MAP_WIDTH.value - 2)
        new_coords = Coordinate(x, y)

        if new_coords not in check_list:
            return new_coords
