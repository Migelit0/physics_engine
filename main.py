import json
import sys

import pygame
from PyQt5 import QtWidgets

import design
from consts import WIDTH, HEIGHT, FPS, MENU_SIZE, BALL_SIZE, TAB
from core import World, get_config_dict


class QtApp(QtWidgets.QMainWindow, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data = get_config_dict()

        self.k_slider.setValue(self.data['k_slider'])
        self.time_slider.setValue(self.data['time_slider'])
        self.mass_slider.setValue(self.data['mass_slider'])
        self.x_slider.setValue(self.data['x_slider'])
        self.y_slider.setValue(self.data['y_slider'])

        self.k_slider.valueChanged[int].connect(self.change_values)  # В ПРОЦЕНТАХ ВВОД ПАМАТУШТА ТАК УДОБНЕЙ
        self.time_slider.valueChanged[int].connect(self.change_values)
        self.mass_slider.valueChanged[int].connect(self.change_values)
        self.x_slider.valueChanged[int].connect(self.change_values)
        self.y_slider.valueChanged[int].connect(self.change_values)

        self.save_button.clicked.connect(self.save_json)
        self.color_button.clicked.connect(self.change_color)

    def change_values(self, value):  # записать во временный json файл значения всех слайдеров
        name = self.sender().objectName()
        self.data[name] = value

    def save_json(self):
        json_data = json.dumps(self.data)
        with open('temp/config.json', 'w') as file:
            file.write(json_data)

    def change_color(self):
        color = QtWidgets.QColorDialog.getColor()
        rgb = color.getRgb()
        color_list = [rgb[0], rgb[1], rgb[2]]  # генератор списков? не
        self.data['rgb'] = color_list


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    window = QtApp()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


def init_app():
    all_bodies = []
    mass = 10 ** 9
    # all_bodies.append(Body(0, mass, (300, 650), Vector((0, 0)), (255, 0, 0)))  # красный
    # all_bodies.append(Body(1, mass, (550, 300), Vector((0, 0)), (0, 255, 0)))  # зеленый
    # all_bodies.append(Body(2, mass, (600, 550), Vector((0, 0)), (0, 0, 255)))  # синий
    # all_bodies.append(Body(3, mass, (100, 100), Vector((0, 0)), (255, 100, 100)))
    # all_bodies.append(Body(4, mass, (300, 300), Vector((0, 0)), (128, 128, 128)))
    # all_bodies.append(Body(3, mass, (100, 100), Vector((0, 0)), (255, 255, 255)))
    # all_bodies.append(Body(4, mass * 10**2, (300, 300), Vector((0, 0)), (0, 0, 0)))

    # PyGame init:
    pygame.init()
    size = WIDTH + MENU_SIZE + BALL_SIZE, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    return all_bodies, screen, clock


if __name__ == '__main__':
    all_bodies, screen, clock = init_app()
    game = World(all_bodies)

    running = True
    is_modeling = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    coords = event.pos  # а может ( y, x )
                    params = get_config_dict()
                    mass, color = params['mass_slider'], params['rgb'],
                    x_vel, y_vel = params['x_slider'], params['y_slider']
                    game.create_body(mass, x_vel, y_vel, coords, color)
                if event.button == 2 or event.button == 3:
                    is_modeling = not is_modeling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # is_modeling = not is_modeling
                    run_app()
                    params = get_config_dict()
                    game.get_data_from_config(params)
                    # ЗАПИСАТЬ В КЛАСС ИГРЫ  К/100, А НЕ ПРОСТО К ТК ОН В ПРОЦЕНТАХ /\

        screen.fill((0, 0, 0))
        for elem in game.bodies:  # отрисовывание всех тел и отскок
            pygame.draw.circle(screen, elem.color, elem.coords, BALL_SIZE)
            k = game.k
            # TODO: нормальное отталкивание (то есть размеры тел) и тогда убрать болл сайз отсюда вообще
            # для версии без боллсайза см ранее 27.08
            if elem.coords[0] <= BALL_SIZE or elem.coords[0] >= WIDTH:  # стукнулся в лево или право
                elem.velocity.coords = (-1 * elem.velocity.coords[0] * k, elem.velocity.coords[1])
                if elem.coords[0] <= BALL_SIZE:  # если слишком влево
                    elem.coords = (BALL_SIZE + 1, elem.coords[1])
                if elem.coords[0] >= WIDTH:  # если слишком вправо
                    elem.coords = (WIDTH - 1, elem.coords[1])
            if elem.coords[1] <= BALL_SIZE or elem.coords[1] >= HEIGHT - BALL_SIZE:  # стукнулся в низ или верх
                elem.velocity.coords = (elem.velocity.coords[0], elem.velocity.coords[1] * -1 * k)
                if elem.coords[1] <= BALL_SIZE:  # слишком вверх
                    elem.coords = (elem.coords[0], BALL_SIZE + 1)
                if elem.coords[1] >= HEIGHT - BALL_SIZE:  # слишком вниз
                    elem.coords = (elem.coords[0], HEIGHT - BALL_SIZE - 1)

        # отрисовка красивишных центров
        for elem in game.bodies:
            pygame.draw.circle(screen, (0, 0, 0), elem.coords, 4)
            pygame.draw.circle(screen, (255, 255, 255), elem.coords, 3)

            # отрисовка вектора скорости (пусть это не будет работать)
            pygame.draw.line(screen, (255, 0, 0), elem.coords,  # (elem.coords[0] * 10, elem.coords[1] * 10),
                             (elem.coords[0] + elem.force.get_x(), elem.coords[1] + elem.force.get_y()), 2)

            # отрисовка центра масс системы
            pygame.draw.circle(screen, (0, 0, 0), game.center_cords, 6)
            pygame.draw.circle(screen, (255, 255, 255), game.center_cords, 5)

            # отрисовка отображения параметров:
            pygame.draw.line(screen, (255, 255, 255), (WIDTH + BALL_SIZE, 0), (WIDTH + BALL_SIZE, HEIGHT), 5)
            params = get_config_dict()
            param_keys = ['k_slider', 'time_slider', 'mass_slider']
            step = HEIGHT // (len(param_keys) + 1)

            font = pygame.font.Font(None, 23)
            for i in range(len(param_keys)):  # емае че происходит (взято из My_Genesis) (даже оптимизировал чето)
                font_renderer = font.render(f'{param_keys[i]} : {params[param_keys[i]]}', 1, (255, 255, 255))
                rect = font_renderer.get_rect()
                rect.top = step * (i + 1)
                rect.x = WIDTH + BALL_SIZE + TAB  # ну опять же убрать боллсайз
                screen.blit(font_renderer, rect)

            if is_modeling:
                try:  # если ошибка в вычислениях (обычно когда нет тел)
                    game.count_all_forces_and_change_velocities()
                except Exception:
                    print(f'NUMBER OF BODIES: {len(game.bodies)}')

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
