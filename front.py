import pygame
from consts import WIDTH, HEIGHT
from core import World, Body
from structures import Vector

if __name__ == '__main__':
    all_bodies = []
    mass = 10**9
    all_bodies.append(Body(0, mass * 10**2, (300, 600), Vector((0, 0))))
    all_bodies.append(Body(1, mass, (900, 300), Vector((0, 0))))
    all_bodies.append(Body(2, mass, (900, 900), Vector((0, 0))))
    game = World(all_bodies)

    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for elem in game.bodies:
            pygame.draw.circle(screen, (255, 0, 0), elem.coords, 20)

        game.count_all_forces_and_change_velocities()

        pygame.display.flip()
    pygame.quit()
