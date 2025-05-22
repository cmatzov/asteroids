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

    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    image = pygame.image.load("assets/images/space.jpg").convert()
    clock = pygame.time.Clock()

    drawables = pygame.sprite.Group()
    updatables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    map = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatables, drawables)
    Boss.containers = (asteroids, updatables, drawables)
    Player.containers = (drawables, updatables)
    AsteroidField.containers = (map)
    Shot.containers = (shots, drawables, updatables)

    dt = 0
    points = 0
    boss_points = 100
    wait_time = 0
    game = "running"

    player = Player(width / 2, height / 2)
    asteroidField = AsteroidField(player.position, width, height)
    game_over = Text("game over", (width // 2, height // 2), 96, (255, 255, 0))
    press_key = Text("press any key to continue...", (width // 2, height // 2), 48, (255, 255, 0))
    score = Text(f"score: {points}", (100, height - 20), 30, (255, 255, 0))
    lives = Text(f"lives: {player.lives}", (width - 100, height - 20), 30, (255, 255, 0))

    while True:
        if game == "running":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            esc_key = pygame.key.get_pressed()
            if esc_key[pygame.K_ESCAPE]:
                sys.exit()

            updatables.update(dt)
            asteroidField.update(player.position)
            asteroidField.spawn(dt, Asteroid)

            screen.blit(image, (0, 0))

            score.draw(screen, 0)
            lives.draw(screen, 0)

            if points >= boss_points:
                asteroidField.spawn(dt, Boss, ignore_timer=True)
                boss_points += 100

            for asteroid in asteroids:
                asteroidField.clear(asteroid, width, height)
                if asteroid.collision(player) == 1:
                    player.lives -= 1
                    lives.update_text(f"Lives: {player.lives}")
                    asteroid.kill()
                    if player.lives == 0:
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
                    asteroidField.clear(shot, width, height)
                    if asteroid.collision(shot) == 1:
                        shot.kill()
                        asteroid.health -= shot.damage
                        if asteroid.health == 0:
                            points += asteroid.update_score(asteroid.radius)
                            asteroid.split()
                            score.update_text(f"Score: {points}")

            for drawable in drawables:
                drawable.draw(screen)

            pygame.display.flip()
            dt = clock.tick(60) / 1000

        elif game == "stopped":
            score = Text(f"Your score: {points}", (width // 2, height // 2), 30, (255, 255, 0))
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