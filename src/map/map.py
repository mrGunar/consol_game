from conf.map_config import MapConfig
from src.coordintate.coordinator import Coordinate
from src.objects.map_objects import EmptyCell
from src.objects.monster import Monster
from src.objects.player import Player
from src.map.fields import FieldsCreator


class Map:
    def __init__(self) -> None:
        self._fields = None
        self._monsters = None
        self._player = None

        self.map_actions = MapAction(self)

    @property
    def fields(self):
        return self._fields

    def add_fields(self, fields=None):
        self._fields = FieldsCreator().create_fields()
        return self

    def add_monsters(self, monsters):
        self._monsters = monsters
        return self

    def add_player(self, player):
        self._player = player
        return self


class MapAction:
    def __init__(self, _map):
        self.map = _map

    def move_object(self, obj, old_coords, new_coords):
        obj2 = self.map.fields[new_coords]

        self.check_objects_intersections(obj, obj2)

        self.map.fields[old_coords] = EmptyCell()
        self.map.fields[new_coords] = obj

    def check_objects_intersections(self, obj_one, obj_two):
        if (
            isinstance(obj_one, Player)
            and isinstance(obj_two, Monster)
            or isinstance(obj_two, Player)
            and isinstance(obj_one, Monster)
        ):
            print("~~YOU LOSE!~~")
            exit()

    def show_map(self) -> None:
        for i in range(MapConfig.MAP_HEIGHT.value):
            for j in range(MapConfig.MAP_WIDTH.value):
                print(self.map.fields[Coordinate(i, j)].icon, end=" ")
            print()

    def get_empty_cells_coords(self) -> list[Coordinate]:
        return [
            coord
            for coord, cell in self.map.fields.items()
            if isinstance(cell, EmptyCell)
        ]

    def get_player_coords(self) -> Coordinate:
        return [
            coord for coord, cell in self.map.fields.items() if isinstance(cell, Player)
        ][0]

    def get_monster_coords(self, monster):
        return [coord for coord, cell in self.map.fields.items() if cell is monster][0]
