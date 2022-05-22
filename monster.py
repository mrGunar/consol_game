from conf import Config
from placeholder import Object


class Monster(Object):
    def __init__(self, x=None, y=None) -> None:
        super().__init__(is_alive=True, is_object=False)
        self.icon = Config.MONSTER_ICON.value

    @classmethod
    def create_monster(cls):
        return Monster()
    
    def kill(self):
        self._is_alive = False
        self.icon = Config.EMPTY_CELL.value
