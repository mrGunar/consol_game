import math
from src.coordintate.coordinator import Coordinate


def get_distance_betwen_two_point(point_one: Coordinate, point_two: Coordinate) -> int:
    x1, y1 = point_one.x, point_one.y
    x2, y2 = point_two.x, point_two.y

    return round(math.sqrt((abs(x1 - x2)) ** 2 + (abs(y1 - y2)) ** 2), 1)


def get_coords_from_dict(dd: dict) -> Coordinate | None:
    min_v = math.inf
    min_coords = None

    for k, v in dd.items():
        if v < min_v:
            min_coords = k
            min_v = v
    if min_coords is not None:
        return Coordinate(*min_coords)
