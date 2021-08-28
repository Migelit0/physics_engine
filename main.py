import sys

import pygame
from PyQt5 import QtWidgets

from QtSettingsApp import QtSettingsApp
from consts import WIDTH, HEIGHT, FPS, MENU_SIZE, BALL_SIZE, TAB, BIGGER
from core import World, get_config_dict


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    window = QtSettingsApp()
    window.show()  # Показываем окно
    window.save_json()
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


def riso2ch(screen):
    screen.fill((0, 0, 0))

    # отрисовка тел
    for elem in game.bodies:
        pygame.draw.circle(screen, elem.color, elem.coords, BALL_SIZE)

    for elem in game.bodies:
        # отрисовка красивишных центров
        pygame.draw.circle(screen, (0, 0, 0), elem.coords, 4)
        pygame.draw.circle(screen, (255, 255, 255), elem.coords, 3)

        # ОПАСНО НЕ ВХОДИТЬ МНОГО СТРЕЛОЧЕч

        # отрисовка вектора СКОРОСТИ ПОМНОЖЕННО1 НА УВЕЛИЧЕСНИЕ
        temp_velocity = elem.velocity * BIGGER * 0.5**4
        pygame.draw.line(screen, (0, 0, 255), elem.coords,  # (elem.coords[0] * 10, elem.coords[1] * 10),
                         (elem.coords[0] + temp_velocity.get_x(), elem.coords[1] + temp_velocity.get_y()), 2)

        # отрисовка вектора УСКОРЕНИЯ * УВЕЛИЧЕНИЕ
        temp_a = elem.force * BIGGER#**1.5   # В СИЛЕ ТЕЛА ЛЕЖИТ УСКОРЕНИЯ ПОТОМУ ЧТО Я В САМОЛЕТЕ И ХЗ КАК ПЕРЕВОДИТСЯ
        print(temp_a.coords)
        pygame.draw.line(screen, (255, 0, 0), elem.coords,
                         (elem.coords[0] + temp_a.get_x(), elem.coords[1] + temp_a.get_y()), 2)

        # отрисовка вектотра силы
        pygame.draw.line(screen, (0, 255, 0), elem.coords,
                         (elem.coords[0] + elem.force.get_x(), elem.coords[1] + elem.force.get_y()), 2)


        # ОПАСНОСТЬ МИНОВАЛА

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
            rect.x = WIDTH + BALL_SIZE + TAB  # TODO: ну опять же убрать боллсайз
            screen.blit(font_renderer, rect)


def body_creator(coords):
    params = get_config_dict()
    mass, color = params['mass_slider'], params['rgb'],
    x_vel, y_vel = params['x_slider'], params['y_slider']
    game.create_body(mass, x_vel, y_vel, coords, color)

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
                    body_creator(event.pos)
                if event.button == 2 or event.button == 3:
                    is_modeling = not is_modeling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # is_modeling = not is_modeling
                    run_app()
                    params = get_config_dict()
                    game.get_data_from_config(params)
                    # ЗАПИСАТЬ В КЛАСС ИГРЫ  К/100, А НЕ ПРОСТО К ТК ОН В ПРОЦЕНТАХ /\

        if is_modeling:
            try:  # если ошибка в вычислениях (обычно когда нет тел)
                game.count_all_forces_and_change_velocities()
            except Exception:
                print(f'NUMBER OF BODIES: {len(game.bodies)}')

        game.check_coords()  # проверка всех координат тел на предмет вылета и отскока
        riso2ch(screen)  # отрисовка всего
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
