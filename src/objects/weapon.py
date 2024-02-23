from src.coordintate.coordinator import Coordinate
from src.objects.object import Object


class WeaponObject(Object):
    def __init__(self, coords: Coordinate = Coordinate(None, None)) -> None:
        super().__init__(coords)
