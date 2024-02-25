from conf.map_config import MapConfig
from src.games_types import Direction


class Player:
    def __init__(self) -> None:
        self.bullet = 0
        self.icon = MapConfig.HUMAN_ICON.value
        self.last_direction = Direction.LEFT
        self._is_alive = True

    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1

    def get_bullet(self, count):
        self.bullet += count

    def kill(self) -> None:
        self._is_alive = False


def create_player():
    return Player()
