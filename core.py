import json
from math import sqrt

from consts import G
from structures import Vector


class Body:
    def __init__(self, id: int, mass: float, coords: tuple, velocity: Vector, color: tuple, force: Vector):
        self.id = id
        self.mass = mass
        self.coords = coords
        self.velocity = velocity
        self.color = color
        self.force = force

    def update_force(self, new_force: Vector):
        self.force = new_force

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


class World:  # TODO: избавиться от констант и записать это в селф
    def __init__(self, bodies: list):
        self.bodies = bodies
        self.center_cords = (0, 0)
        self.get_data_from_config(get_config_dict())

    def count_abc_force_for_two_bodies(self, body_1: Body, body_2: Body):
        return G * body_1.mass * body_2.mass / ((body_1 ^ body_2) ** 2)

    def count_all_forces_and_change_velocities(self):
        all_force = Vector((0, 0))
        for body_main in self.bodies:
            equal_force = Vector((0, 0))
            for body in self.bodies:
                if body_main != body:   # чтобы тело не действовало само на себя а то деление на 0 очевидно
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
            delta_velocity = a * self.delta_time
            body_main.add_velocity(delta_velocity)

            body_main.update_force(equal_force)  # обновляем силу действующую на тело
            all_force = equal_force + all_force  # в суму всех сил добавляем текущую

        for body in self.bodies:
            body.update_coords()

        print(all_force.coords)

        self.count_center_coords()

    def get_new_id(self):
        if len(self.bodies) == 0:  # нет тел
            return 0
        return sorted(self.bodies, key=lambda x: x.id)[-1].id + 1

    def count_center_coords(self):
        center = Vector((0, 0))
        all_mass = 0
        for body in self.bodies:
            center = center + Vector(body.coords) * body.mass
            all_mass += body.mass
        self.center_cords = (center / all_mass).coords

    def create_body(self, mass: float, x_vel: int, y_vel: int, coords: tuple, color: tuple):
        vel = Vector((x_vel, y_vel))
        body = Body(self.get_new_id(), mass, coords, vel, color, Vector((0, 0)))
        self.bodies.append(body)

    def get_data_from_config(self, param_dict):  # полезно так полезно
        # внемание говнокод
        self.k = param_dict['k_slider'] / 100
        self.delta_time = param_dict['time_slider']
        # pass  # кпд, тик и все такое записать в переменные ИЗ СЛОВАРЯ


def get_config_dict():
    with open('temp/config.json') as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    pass
