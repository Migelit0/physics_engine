from math import sqrt, atan, sin, cos, pi, atan2
from consts import G, DELTA_TIME
from structures import Vector


class Body:
    def __init__(self, id: int, mass: float, coords: tuple, velocity: Vector, color: tuple):
        self.id = id
        self.mass = mass
        self.coords = coords
        self.velocity = velocity
        self.color = color

    def __eq__(self, other):
        return self.id == other.id

    def __neg__(self, other):
        return self.id != other.id

    def __xor__(self, other):
        x1, y1 = other.coords
        x, y = self.coords
        return sqrt((x1 - x) ** 2 + (y1 - y) ** 2)

    def add_velocity(self, delta_velocity: Vector):
        self.velocity = self.velocity + delta_velocity

    def update_coords(self):
        dx, dy = self.velocity.coords
        self.coords = (self.coords[0] + dx, self.coords[1] + dy)


class World:
    def __init__(self, bodies: list):
        self.bodies = bodies

    def count_abc_force_for_two_bodies(self, body_1: Body, body_2: Body):
        return G * body_1.mass * body_2.mass / ((body_1 ^ body_2) ** 2)

    def count_all_forces_and_change_velocities(self):
        all_force = Vector((0, 0))
        for body_main in self.bodies:
            for body in self.bodies:
                equal_force = Vector((0, 0))
                if body_main != body:
                    x1, y1 = body.coords
                    x, y = body_main.coords

                    dx, dy = x1 - x, y1 - y
                    long = sqrt(dx ** 2 + dy ** 2)  # это типа гипотенуза треугольника
                    sina = dy / long
                    cosa = dx / long

                    # alpha = atan2(sina,  cosa)  # пипец вообще умно
                    # sina = sin(alpha)
                    # cosa = cos(alpha)

                    abc_force = self.count_abc_force_for_two_bodies(body_main, body)
                    force = Vector((abc_force * cosa, abc_force * sina))
                    equal_force = equal_force + force


                a = equal_force / body_main.mass
                # print(a.coords)
                delta_velocity = a * DELTA_TIME
                body_main.add_velocity(delta_velocity)
                body_main.update_coords()

                all_force = equal_force + all_force
        print(all_force.coords)


if __name__ == '__main__':
    pass
