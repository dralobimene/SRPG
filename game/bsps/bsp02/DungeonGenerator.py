import random
import math
import os
from datetime import datetime


from .Room import Room
from .Path import Path
from .DivideDirection import DivideDirection
from .TileTypes import TileTypes
from .MapPartition import MapPartition


class DungeonGenerator:
    def __init__(self):
        self.tile_dict = None

    def __write_room_to_map(self, map: list, map_width: int, room: Room) -> list:
        if room is None:
            return map
        map_height = math.trunc(len(map) / map_width)
        for y in range(room.height):
            for x in range(room.width):
                map_x = x + room.x
                map_y = y + room.y
                if (map_x < 0 or map_x >= map_width):
                    continue
                if (map_y < 0 or map_y >= map_height):
                    continue
                map_i = self.index_from_coordinates(map_x, map_y, map_width)
                map[map_i] = self.tile_dict.get(TileTypes.FLOOR)

    def __write_path_to_map(self, map: list, map_width: int, path: Path) -> list:
        if path is None:
            return map
        map_height = math.trunc(len(map) / map_width)
        for x, y in path.path:
            if x < 0 or x >= map_width:
                continue
            if y < 0 or y >= map_height:
                continue
            map_i = self.index_from_coordinates(x, y, map_width)
            map[map_i] = self.tile_dict.get(TileTypes.PATH)

    def __write_partitions_to_map(self, map: list, map_width: int, partition: MapPartition) -> list:
        self.__recurse_partition_to_map(map, map_width, partition)

    def __recurse_partition_to_map(self, map: list, map_width: int, partition: MapPartition) -> MapPartition:
        if partition.room is not None:
            self.__write_room_to_map(map, map_width, partition.room)
        if partition.path is not None:
            self.__write_path_to_map(map, map_width, partition.path)
        if partition.children[0] is not None:
            self.__recurse_partition_to_map(
                map, map_width, partition.children[0])
        if partition.children[1] is not None:
            self.__recurse_partition_to_map(
                map, map_width, partition.children[1])

    def __create_partitions(self, x: int, y: int, width: int, height: int, divisions: int) -> MapPartition:
        partition = MapPartition(x, y, width, height)
        self.__recurse_partitions(partition, divisions)
        return partition

    def __recurse_partitions(self, partition: MapPartition, divisions: int) -> None:
        if divisions == 0:
            partition.create_room()  # create a room in each of the final level partitions
            # create a key point in each room to ensure accessibility
            partition.create_key_point()
            return
        aspect_ratio = partition.width / partition.height
        divide_direction = DivideDirection(
            1) if aspect_ratio > 1 else DivideDirection(2)
        if aspect_ratio == 1:
            divide_direction = DivideDirection(random.randint(1, 2))
        partition_1, partition_2 = partition.create_children(divide_direction)
        if partition_1 is not None:
            self.__recurse_partitions(partition_1, divisions - 1)
        if partition_2 is not None:
            self.__recurse_partitions(partition_2, divisions - 1)
        partition.create_path_between_children()
        partition.create_key_point()

    def generate_default_tile_dict(self) -> dict:
        self.tile_dict = {
            TileTypes.EMPTY: 0,
            TileTypes.FLOOR: 1,
            TileTypes.PATH: 2,
            TileTypes.WALL: 3,
            TileTypes.DOOR: 4
        }
        return self.tile_dict

    def generate_map(self, width: int, height: int, divisions: int = 4) -> list:
        """
        Les fichiers générés sont stockés dans le repertoire: "temp_txt_files".
        """
        if (self.tile_dict is None):
            self.generate_default_tile_dict()
        generated_map = [self.tile_dict.get(TileTypes.EMPTY)]*(width * height)
        map_partitions = self.__create_partitions(
            0, 0, width, height, divisions)
        self.__write_partitions_to_map(generated_map, width, map_partitions)
        return (generated_map, map_partitions)

    def index_from_coordinates(self, x: int, y: int, width: int) -> int:
        return int(x + math.trunc(y * width))

    def coordinates_from_index(self, i: int, width: int) -> tuple:
        return (i % width, math.trunc(i / width))

    def write_map_to_file(self, map, map_width, unique_id):
        # Obtention de la date et l'heure actuelles
        current_time = datetime.now()

        # Formatage de la date et l'heure
        formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S")

        # Création du nom de fichier
        file_name = f"{formatted_time}_{unique_id}.txt"

        # Nom du dossier qui va contenir les fichiers txt temporaires.
        folder_name = "temp_txt_files/"

        # Chemin complet vers le fichier
        full_file_path = os.path.join(folder_name, file_name)

        #
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            # print("'temp_txt_files' path exists")
            pass
        else:
            print("temp_txt_files does not exist")
            print("We need to create it.")

            try:
                os.mkdir(folder_name)
            except FileExistsError:
                print(f"Le répertoire {folder_name} existe déjà.")

        with open(full_file_path, "w") as f:
            for i, tile in enumerate(map):
                if i % map_width == 0:
                    f.write("\n")
                if tile == self.tile_dict.get(TileTypes.FLOOR) or tile == self.tile_dict.get(TileTypes.PATH):
                    f.write(".")
                else:
                    f.write("#")

    def is_reachable_02(self, dungeon_map, map_width):
        visited = [False] * len(dungeon_map)
        stack = []

        for i, tile in enumerate(dungeon_map):
            if tile == self.tile_dict.get(TileTypes.FLOOR) or tile == self.tile_dict.get(TileTypes.PATH):
                start = i
                break

        stack.append(start)

        while stack:
            pos = stack.pop()
            if visited[pos] or dungeon_map[pos] == self.tile_dict.get(TileTypes.WALL):
                continue
            visited[pos] = True

            x, y = self.coordinates_from_index(pos, map_width)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < map_width and 0 <= ny < len(dungeon_map) // map_width:
                    next_pos = self.index_from_coordinates(nx, ny, map_width)
                    stack.append(next_pos)

        return all(visited[i] or dungeon_map[i] == self.tile_dict.get(TileTypes.WALL) for i in range(len(dungeon_map)))
