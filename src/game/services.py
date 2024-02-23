from conf.map_config import MapConfig
from src.services import services
from src.coordintate.coordinator import Coordinate


def get_next_coord_for_monster(map, player, monster_coords: Coordinate) -> Coordinate:
    nei = [(1, 1), (1, 0), (-1, 0), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]

    res = {}
    for i, j in nei:
        dx = monster_coords.x - i
        dy = monster_coords.y - j
        if (
            0 < dx < MapConfig.MAP_HEIGHT.value
            and 0 < dy < MapConfig.MAP_WIDTH.value
            and map.fields[dx][dy] == MapConfig.EMPTY_CELL.value
        ):
            res.update(
                {
                    (dx, dy): services.get_distance_betwen_two_point(
                        player.get_coords(), Coordinate(dx, dy)
                    )
                }
            )
    coords = services.get_coords_from_dict(res)
    return coords if coords is not None else monster_coords


def is_move_valid(coords: Coordinate, _map) -> bool:
    return (
            0 < coords.x < MapConfig.MAP_HEIGHT.value - 1
            and 0 < coords.y < MapConfig.MAP_WIDTH.value - 1
            and _map.fields[coords.x][coords.y] != MapConfig.BORDER_CELL.value
            )

def find_monster_with_coord(x: int, y: int, map) -> object:
    for m in map.monsters:
        if (x, y) == (m.x, m.y):
            return m