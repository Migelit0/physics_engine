import json
from math import sqrt

from consts import G, BALL_SIZE, WIDTH, HEIGHT, MAX_TRAJECTORY_LEN, TRAJECTORY_UPDATE_TIME
from structures import Vector


class Body:
    def __init__(self, id: int, mass: float, coords: tuple, velocity: Vector, color: tuple):
        self.id = id
        self.mass = mass
        self.coords = coords
        self.velocity = velocity
        self.color = color
        self.force = Vector((0, 0))
        self.speedup = Vector((0, 0))
        self.trajectory = []

    def update_force(self, new_force: Vector):
        self.force = new_force

    def update_speedup(self, new_speedup: Vector):
        self.speedup = new_speedup

    def update_trajectory(self):
        if len(self.trajectory) == MAX_TRAJECTORY_LEN:
            del self.trajectory[0]

        self.trajectory.append(self.coords)

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
        self.update_num = 0

    def count_abc_force_for_two_bodies(self, body_1: Body, body_2: Body):
        return G * body_1.mass * body_2.mass / ((body_1 ^ body_2) ** 2)

    def count_forces_for_body(self, body_main):
        equal_force = Vector((0, 0))
        for body in self.bodies:
            if body_main != body:  # чтобы тело не действовало само на себя а то деление на 0 очевидно
                x1, y1 = body.coords
                x, y = body_main.coords

                dx, dy = x1 - x, y1 - y
                long = sqrt(dx ** 2 + dy ** 2)  # это типа гипотенуза треугольника
                sina = dy / long
                cosa = dx / long

                abc_force = self.count_abc_force_for_two_bodies(body_main, body)
                force = Vector((abc_force * cosa, abc_force * sina))
                equal_force = equal_force + force
        return equal_force

    def count_all_forces_and_change_velocities(self):
        all_force = Vector((0, 0))
        for body_main in self.bodies:
            equal_force = self.count_forces_for_body(body_main)

            a = equal_force / body_main.mass
            delta_velocity = a * self.delta_time
            body_main.add_velocity(delta_velocity)

            body_main.update_speedup(a)  # обновляем ускорение тела
            body_main.update_force(equal_force)  # щбновляем силу действующую на тело

            if self.update_num == TRAJECTORY_UPDATE_TIME:
                body_main.update_trajectory()
            all_force = equal_force + all_force  # в сумму всех сил добавляем текущую

        for body in self.bodies:
            body.update_coords()

        if self.update_num == TRAJECTORY_UPDATE_TIME:
            self.update_num = 0
        else:
            self.update_num += 1

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
        body = Body(self.get_new_id(), mass, coords, vel, color)
        self.bodies.append(body)

    def get_data_from_config(self, param_dict):  # полезно так полезно
        # внемание говнокод
        self.k = param_dict['k_slider'] / 100
        self.delta_time = param_dict['time_slider']
        # pass  # кпд, тик и все такое записать в переменные ИЗ СЛОВАРЯ

    def check_coords(self):
        for elem in self.bodies:  # отрисовывание всех тел и отскок
            k = self.k  # спасибо спасибо спасибо спасибо спасибо спасибо спасибо спасибо спасибо спасибо спасибо
            # TODO: нормальное отталкивание (то есть размеры тел) и тогда убрать болл сайз отсюда вообще
            # для версии без боллсайза см ранее 27.08
            if elem.coords[0] <= BALL_SIZE or elem.coords[0] >= WIDTH:  # стукнулся в лево или право
                elem.velocity.coords = (-1 * elem.velocity.get_x() * k, elem.velocity.get_y() * k)
                if elem.coords[0] <= BALL_SIZE:  # если слишком влево
                    elem.coords = (BALL_SIZE + 1, elem.coords[1])
                if elem.coords[0] >= WIDTH:  # если слишком вправо
                    elem.coords = (WIDTH - 1, elem.coords[1])
            if elem.coords[1] <= BALL_SIZE or elem.coords[1] >= HEIGHT - BALL_SIZE:  # стукнулся в низ или верх
                elem.velocity.coords = (elem.velocity.get_x() * k, elem.velocity.get_y() * -1 * k)
                if elem.coords[1] <= BALL_SIZE:  # слишком вверх
                    elem.coords = (elem.coords[0], BALL_SIZE + 1)
                if elem.coords[1] >= HEIGHT - BALL_SIZE:  # слишком вниз
                    elem.coords = (elem.coords[0], HEIGHT - BALL_SIZE - 1)


def get_config_dict():
    with open('temp/config.json') as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    pass
