import pygame
import sys
from player import Player
from asteroid import Asteroid
from bossAsteroid import Boss
from asteroidfield import AsteroidField
from constants import *
from bullets import Shot
from text import Text

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    drawables = pygame.sprite.Group()
    updatables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatables, drawables)
    Boss.containers = (asteroids, updatables, drawables)
    Player.containers = (drawables, updatables)
    AsteroidField.containers = (updatables)
    Shot.containers = (shots, drawables, updatables)

    dt = 0
    points = 0
    remaining_lives = 3
    wait_time = 0
    game = "running"

    asteroidField = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game_over = Text("Game Over", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 96, (255, 0, 0))
    press_key = Text("Press Enter to Play Again or any other key to exit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 48, (255, 0, 0))
    score = Text(f"Score: {points}", (50, SCREEN_HEIGHT - 20), 30, (255, 0, 0))
    lives = Text(f"Lives: {remaining_lives}", (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20), 30, (255, 0, 0))

    while True:
        if game == "running":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            updatables.update(dt)

            screen.fill("black")

            score.draw(screen, 0)
            lives.draw(screen, 0)

            for asteroid in asteroids:

                asteroidField.clear(asteroid)

                if asteroid.collision(player) == 1:
                    remaining_lives -= 1
                    lives.update_text(f"Lives: {remaining_lives}")
                    asteroid.kill()
                    if remaining_lives == 0:
                        game = "stopped"

                normals = [ast for ast in asteroids if not isinstance(ast, Boss)]
                bosses = [ast for ast in asteroids if isinstance(ast, Boss)]
                for boss in bosses:
                    for norm in normals:
                        if boss.collision(norm):
                            boss.bounce_away_other(norm)

                for norm in normals:
                    if norm == asteroid:
                        pass
                    if norm.collision(asteroid) == 1:
                        asteroid.bounce(norm)

                for other in asteroids:
                    if asteroid == other:
                        pass
                    if asteroid.collision(other) == 1:
                        asteroid.bounce(other)

                for shot in shots:
                    asteroidField.clear(shot)

                    if asteroid.collision(shot) == 1:
                        shot.kill()
                        asteroid.hits += 1
                        if asteroid.hits == asteroid.max_hits:
                            points += asteroid.update_score(asteroid.radius)
                            asteroid.split()
                            score.update_text(f"Score: {points}")

            for drawable in drawables:
                drawable.draw(screen)

            pygame.display.flip()
            dt = clock.tick(60) / 1000

        elif game == "stopped":
            score = Text(f"Your score: {points}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 30, (255, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill("black")

            game_over.draw(screen, 50)
            press_key.draw(screen, -50)
            score.draw(screen, -100)

            wait_time += dt
            if wait_time > 1:
                keys = pygame.key.get_pressed()
                if any(keys):
                    sys.exit()

            pygame.display.flip()
            dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()