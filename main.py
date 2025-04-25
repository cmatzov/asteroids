import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from bullets import Shot
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    drawables = pygame.sprite.Group()
    updatables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatables, drawables)
    Player.containers = (drawables, updatables)
    AsteroidField.containers = (updatables)
    Shot.containers = (shots, drawables, updatables)

    asteroidField = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatables.update(dt)

        screen.fill("black")

        for asteroid in asteroids:
            if asteroid.collision(player) == True:
                print("Game Over")
                sys.exit()

            for shot in shots:
                if asteroid.collision(shot) == True:
                    shot.kill()
                    asteroid.split()

        for drawable in drawables:
            drawable.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()