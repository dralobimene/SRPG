
from random import randint
from bsps.bsp01.Rect import Rect


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walkable = [[False for _ in range(height)] for _ in range(width)]

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.walkable[x][y] = True

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.walkable[x][y] = True

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.walkable[x][y] = True

    def is_blocked(self, x, y):
        return not self.walkable[x][y]

    def make_map(self, max_rooms, room_min_size, room_max_size):
        rooms = []
        num_rooms = 0
        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)
            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)
                if num_rooms != 0:
                    prev_x, prev_y = rooms[num_rooms - 1].center()
                    new_x, new_y = new_room.center()
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                rooms.append(new_room)
                num_rooms += 1

    def save_map_to_file(self, filename):
        with open(filename, 'w') as f:
            for y in range(self.height):
                for x in range(self.width):
                    if self.is_blocked(x, y):
                        f.write('#')
                    else:
                        f.write('.')
                f.write('\n')
