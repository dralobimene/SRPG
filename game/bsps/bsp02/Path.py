import random


class Path:
    def __init__(self):
        self.path = []

    def connect_points(self, x1: int, y1: int, x2: int, y2: int) -> list:
        """Connect points using L or Z shaped paths"""
        # clear any existing path
        self.path = [(x1, y1)]

        delta_x = x2 - x1
        delta_y = y2 - y1

        distance_x = abs(delta_x)
        distance_y = abs(delta_y)

        x_incr = 0 if distance_x == 0 else delta_x / distance_x
        y_incr = 0 if distance_y == 0 else delta_y / distance_y

        x = x1
        y = y1

        force_decision = 0
        if distance_x == distance_y:
            # if the x any y distances are equal, randomly pick a direction
            force_decision = random.randint(1, 2)

        if force_decision == 1 or distance_x > distance_y:
            bend_point = x1 + (random.randint(0, distance_x) * x_incr)

            while True:
                if x == bend_point:
                    while True:
                        y += y_incr
                        self.path.append((x, y))

                        if y == y2:
                            break

                x += x_incr
                self.path.append((x, y))

                if x == x2:
                    break

        elif force_decision == 2 or distance_x < distance_y:
            bend_point = y1 + (random.randint(0, distance_y) * y_incr)

            while True:
                if y == bend_point:
                    while True:
                        x += x_incr
                        self.path.append((x, y))

                        if x == x2:
                            break

                y += y_incr
                self.path.append((x, y))

                if y == y2:
                    break

        return self.path
