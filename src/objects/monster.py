from conf.map_config import MapConfig


class Monster:
    def __init__(self) -> None:
        self.icon = MapConfig.MONSTER_ICON.value
        self._is_alive = True

    @classmethod
    def create_monster(cls):
        return Monster()

    def kill(self):
        self._is_alive = False


def create_monster():
    return Monster()
