
import math
# Notez le '.' qui indique un import relatif
from .DungeonGenerator import DungeonGenerator


class DungeonFileGenerator:
    def __init__(self, dungeon: DungeonGenerator = None):
        if dungeon is None:
            dungeon = DungeonGenerator()
        self.dungeon = dungeon

    def create_map(self, width: int, height: int):
        map_width, map_height = (math.trunc(
            width / 16), math.trunc(height / 16))
        dm, mp = self.dungeon.generate_map(map_width, map_height, 3)
        return (dm, map_width, mp)

    def generate_map_file(self, unique_id):
        dm, mw, mp = self.create_map(800, 600)
        if self.dungeon.is_reachable_02(dm, mw):
            print(f"Le donjon crée avec le bsp02: {unique_id} est accessible!")
            self.dungeon.write_map_to_file(dm, mw, unique_id)
        else:
            print(
                f"Le donjon crée avec le bsp02: {unique_id} n'est pas accessible!")
