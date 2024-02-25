from conf.map_config import MapConfig
from src.services import services
from src.coordintate.coordinator import Coordinate


def get_next_coord_for_monster(
    _map, player_coords: Coordinate, monster_coords: Coordinate
) -> Coordinate:
    nei = [(1, 1), (1, 0), (-1, 0), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]

    res = {}
    for i, j in nei:
        dx = monster_coords.x - i
        dy = monster_coords.y - j

        d_coords = Coordinate(dx, dy)

        if is_move_valid(d_coords, _map):
            res.update(
                {
                    d_coords: services.get_distance_betwen_two_point(
                        player_coords, d_coords
                    )
                }
            )
    coords = services.get_coords_from_dict(res)
    return coords if coords is not None else monster_coords


def is_move_valid(coords: Coordinate, _map) -> bool:
    return (
        0 < coords.x < MapConfig.MAP_HEIGHT.value - 1
        and 0 < coords.y < MapConfig.MAP_WIDTH.value - 1
        and _map.fields[coords].icon
        in (MapConfig.EMPTY_CELL.value, MapConfig.HUMAN_ICON.value)
    )


def find_monster_with_coord(coords: Coordinate, monsters: list) -> object:
    for monster in monsters:
        if coords == monster.get_coords():
            return monster
