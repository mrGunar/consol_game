from conf.map_config import MapConfig


class EmptyCell:
    def __init__(self):
        self.icon = MapConfig.EMPTY_CELL.value


class Border:
    def __init__(self):
        self.icon = MapConfig.BORDER_CELL.value
