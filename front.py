import sys

import pygame
from PyQt5 import QtWidgets

import design
from consts import WIDTH, HEIGHT, K, FPS
from core import World, Body
from structures import Vector


class QtApp(QtWidgets.QMainWindow, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    window = QtApp()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


def init_app():
    all_bodies = []
    mass = 10 ** 9
    all_bodies.append(Body(0, mass, (300, 650), Vector((0, 0)), (255, 0, 0)))  # красный
    all_bodies.append(Body(1, mass, (890, 300), Vector((0, 0)), (0, 255, 0)))  # зеленый
    all_bodies.append(Body(2, mass, (900, 900), Vector((0, 0)), (0, 0, 255)))  # синий
    # all_bodies.append(Body(3, mass, (100, 100), Vector((0, 0)), (255, 255, 255)))
    # all_bodies.append(Body(4, mass * 10**2, (300, 300), Vector((0, 0)), (0, 0, 0)))
    # game = World(all_bodies)

    # PyGame init:
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # PyQt init
    # QtThread = threading.Thread(target=run_app)
    # QtThread.start()
    # design.runApp()
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtApp()
    # window.show()  # Показываем окно
    # app.exec_()  # и запускаем приложение

    return all_bodies, screen, clock


if __name__ == '__main__':
    all_bodies, screen, clock = init_app()
    # all_bodies.append(Body(3, mass, (100, 100), Vector((0, 0)), (255, 255, 255)))
    # all_bodies.append(Body(4, mass * 10**2, (300, 300), Vector((0, 0)), (0, 0, 0)))
    game = World(all_bodies)

    running = True
    is_modeling = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    coords = event.pos
                    game.create_body()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_modeling = not is_modeling

        screen.fill((0, 0, 0))
        for elem in game.bodies:  # отрисовывание всех тел и отскок
            pygame.draw.circle(screen, elem.color, elem.coords, 20)
            if elem.coords[0] <= 0 or elem.coords[0] >= WIDTH:
                elem.velocity.coords = (-1 * elem.velocity.coords[0] * K, elem.velocity.coords[1])
                if elem.coords[0] <= 0:
                    elem.coords = (1, elem.coords[1])
                if elem.coords[0] >= WIDTH:
                    elem.coords = (WIDTH - 1, elem.coords[1])
            if elem.coords[1] <= 0 or elem.coords[1] >= HEIGHT:
                elem.velocity.coords = (elem.velocity.coords[0], elem.velocity.coords[1] * -1 * K)
                if elem.coords[0] <= 0:
                    elem.coords = (elem.coords[0], 1)
                if elem.coords[0] >= HEIGHT:
                    elem.coords = (elem.coords[0], HEIGHT - 1)

        if is_modeling:
            game.count_all_forces_and_change_velocities()

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
