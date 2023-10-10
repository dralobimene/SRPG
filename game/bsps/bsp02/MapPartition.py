import random
import math

from .Room import Room
from .Path import Path
from .DivideDirection import DivideDirection


class MapPartition:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = (None, None)
        self.room = None
        self.path = None
        self.parent = None

    def create_children(self, divide_direction: DivideDirection, divide_range: float = 0.7) -> tuple:
        modification_factor = ((2 * random.random()) - 1) * divide_range
        if divide_direction is DivideDirection.DIVIDE_X:
            divide_x = math.trunc(
                (self.width / 2) + ((self.width / 2) * modification_factor))
            new_partition_1 = None
            new_partition_2 = None
            if divide_x > 0 and divide_x < self.width:
                new_partition_1 = MapPartition(
                    self.x, self.y, divide_x, self.height)
                new_partition_1.parent = self
                new_partition_2 = MapPartition(
                    self.x + divide_x, self.y, self.width - divide_x, self.height)
                new_partition_2.parent = self
            self.children = (new_partition_1, new_partition_2)
        elif divide_direction is DivideDirection.DIVIDE_Y:
            divide_y = math.trunc((self.height / 2) +
                                  ((self.height / 2) * modification_factor))
            new_partition_1 = None
            new_partition_2 = None
            if divide_y > 0 and divide_y < self.height:
                new_partition_1 = MapPartition(
                    self.x, self.y, self.width, divide_y)
                new_partition_1.parent = self
                new_partition_2 = MapPartition(
                    self.x, self.y + divide_y, self.width, self.height - divide_y)
                new_partition_2.parent = self
            self.children = (new_partition_1, new_partition_2)
        return self.children

    def create_room(self, min_room_size: int = 2, min_cells_from_side: int = 1) -> Room:
        # Generates a room that fits within the partition
        max_room_width = self.width - (2 * min_cells_from_side)
        max_room_height = self.height - (2 * min_cells_from_side)
        if max_room_width < min_room_size or max_room_height < min_room_size:
            return  # if the partition is too small to have a room, don't create one
        room_width = random.randint(min_room_size, max_room_width)
        room_height = random.randint(min_room_size, max_room_height)
        room_x = self.x + \
            random.randint(min_cells_from_side, self.width - room_width - 1)
        room_y = self.y + \
            random.randint(min_cells_from_side, self.height - room_height - 1)
        self.room = Room(room_x, room_y, room_width, room_height)
        return self.room

    def create_key_point(self) -> tuple:
        if self.room is not None:
            key_point_x = self.room.x + random.randint(0, self.room.width - 1)
            key_point_y = self.room.y + random.randint(0, self.room.height - 1)
        elif self.path is not None:
            path_length = len(self.path.path)
            path_point = random.randint(0, path_length - 1)
            key_point_x, key_point_y = self.path.path[path_point]
        else:
            key_point_x = self.x + random.randint(0, self.width - 1)
            key_point_y = self.y + random.randint(0, self.height - 1)
        self.key_point = (key_point_x, key_point_y)
        return self.key_point

    def create_path_between_children(self) -> Path:
        child_0 = self.children[0]
        child_1 = self.children[1]
        if child_0 is not None and child_1 is not None:
            if child_0.key_point is None:
                child_0.create_key_point()
            if child_1.key_point is None:
                child_1.create_key_point()
            self.path = Path()
            x1, y1 = child_0.key_point
            x2, y2 = child_1.key_point
            self.path.connect_points(x1, y1, x2, y2)
            return self.path
