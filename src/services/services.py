import math

def get_distance_betwen_two_point(point_one: tuple, point_two: tuple) -> int:

    x1, y1 = point_one
    x2, y2 = point_two

    return round(math.sqrt((abs(x1-x2)) ** 2 + (abs(y1-y2)) ** 2),1)
    

def get_coords_from_dict(dd: dict) -> tuple:
    min_v = math.inf
    min_coords = None
    

    for k, v in dd.items():
        if v < min_v:
            min_coords = k
            min_v = v

    return min_coords

