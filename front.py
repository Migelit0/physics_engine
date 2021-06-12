import pygame
from consts import WIDTH, HEIGHT, K
from core import World, Body
from structures import Vector

if __name__ == '__main__':
    all_bodies = []
    mass = 10 ** 9
    all_bodies.append(Body(0, mass, (300, 650), Vector((0, 0)), (255, 0, 0)))  # красный
    all_bodies.append(Body(1, mass, (890, 300), Vector((0, 0)), (0, 255, 0)))  # зеленый
    all_bodies.append(Body(2, mass, (900, 900), Vector((0, 0)), (0, 0, 255)))  # синий
    # all_bodies.append(Body(3, mass, (100, 100), Vector((0, 0)), (255, 255, 255)))
    # all_bodies.append(Body(4, mass * 10**2, (300, 300), Vector((0, 0)), (0, 0, 0)))
    game = World(all_bodies)

    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    fps = 144
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for elem in game.bodies:
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

        game.count_all_forces_and_change_velocities()

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
