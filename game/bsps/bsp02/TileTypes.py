import enum


class TileTypes(enum.Enum):
    EMPTY = "empty"
    FLOOR = "floor"
    PATH = "path"
    WALL = "wall"
    DOOR = "door"

