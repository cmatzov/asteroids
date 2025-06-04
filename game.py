import pygame
import sys
from player import Player
from asteroid import Asteroid
from bossAsteroid import Boss
from asteroidfield import AsteroidField
from particles import Particle
from constants import *
from bullets import Shot
from text import Text
from icons import Icons
from powerups import *

class Game():
    def __init__(self):
        pygame.init()

        self.drawables = pygame.sprite.Group()
        self.updatables = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.map = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        Asteroid.containers = (self.asteroids, self.updatables, self.drawables)
        AsteroidField.containers = (self.map)
        Boss.containers = (self.asteroids, self.updatables, self.drawables)
        Player.containers = (self.drawables, self.updatables)
        Shot.containers = (self.shots, self.drawables, self.updatables)
        Particle.containers = (self.particles)
        Shield.containers = (self.powerups)
        BonusLife.containers = (self.powerups)

        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.clock = pygame.time.Clock()

        self.boss_points = 100
        self.wait_time = 0
        self.shield_num = 0

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.player = Player(self.width / 2, self.height / 2, self.screen)
        self.asteroidField = AsteroidField(self.player.position, self.width, self.height)

        self.image = pygame.image.load("assets/images/space.jpg").convert()
        self.shield_icon = Icons("assets/images/shield.png", (30, 52), (30, 30))
        self.heart_icon = Icons("assets/images/heart.png", (20, 3), (50, 50))
        self.score = Text(f"score: {self.player.points}", (100, self.height - 20), 30, (255, 255, 0))
        self.lives = Text(f"x{self.player.lives}", (90, 25), 35, (255, 255, 0))
        self.shields = Text(f"x{self.shield_num}", (90, 65), 35, (255, 255, 0))

    def guid(self):
        self.score.draw(self.screen, 0)
        self.lives.draw(self.screen, 0)
        self.shields.draw(self.screen, 0)
        self.shield_icon.draw(self.screen)
        self.heart_icon.draw(self.screen)
    
    def update_guid(self):
        self.score.update_text(f"Score: {self.player.points}")
        self.lives.update_text(f"x{self.player.lives}")
        self.shield_num = len(self.player.shield_num)
        print(self.shield_num)
        self.shields.update_text(f"x{self.shield_num}")

    def start(self):
        dt = 0
        while True:
            while self.player.lives > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                esc_key = pygame.key.get_pressed()
                if esc_key[pygame.K_ESCAPE]:
                    sys.exit()

                self.updatables.update(dt)
                self.particles.update(dt)
                self.powerups.update(self.player.position)
                self.asteroidField.update(self.player.position)
                self.update_guid()
                self.asteroidField.spawn(dt, Asteroid)
                self.screen.blit(self.image, (0, 0))

                self.play(dt)

                for drawable in self.drawables:
                    drawable.draw(self.screen)
                self.guid()
                self.particles.draw(self.screen)
                self.powerups.draw(self.screen)
                if self.player.shield and self.player.shield.is_active:
                    self.player.shield.draw()
                dt = self.clock.tick(60) / 1000
                pygame.display.flip()
            self.game_over(dt)

    def play(self, dt):
        if self.player.points >= self.boss_points:
            self.asteroidField.spawn(dt, Boss, ignore_timer=True)
            self.boss_points += 100

        for asteroid in self.asteroids:
            self.asteroidField.clear(asteroid, self.width, self.height)
            if self.player.shield:
                self.player.shield.add(Shield.containers)
                if asteroid.collision(self.player.shield) == 1:
                    self.player.shield.hit()
                    asteroid.particle_effect()
                    asteroid.kill()
                    continue
            if asteroid.collision(self.player):
                asteroid.particle_effect()
                self.player.lives -= 1
                asteroid.kill()

            normals = [ast for ast in self.asteroids if not isinstance(ast, Boss)]
            bosses = [ast for ast in self.asteroids if isinstance(ast, Boss)]
            for boss in bosses:
                for norm in normals:
                    if boss.collision(norm):
                        boss.bounce_away_other(norm)
            for norm in normals:
                if norm == asteroid:
                    pass
                if norm.collision(asteroid) == 1:
                    asteroid.bounce(norm)
            for other in self.asteroids:
                if asteroid == other:
                    pass
                if asteroid.collision(other) == 1:
                    asteroid.bounce(other)
            for shot in self.shots:
                self.asteroidField.clear(shot, self.width, self.height)
                if asteroid.collision(shot) == 1:
                    shot.kill()
                    asteroid.particle_effect()
                    asteroid.health -= shot.damage
                    if asteroid.health == 0:
                        self.player.points += asteroid.update_score(asteroid.radius)
                        asteroid.split(self.screen)
        for powerup in self.powerups:
            if isinstance(powerup, BonusLife):
                if self.player.collision(powerup):
                    self.player.lives += 1
                    powerup.kill()
            if powerup.is_active == False and not isinstance(powerup, BonusLife):
                if self.player.collision(powerup):
                    self.player.shield_num.append(powerup)
                    powerup.kill()

    def game_over(self, dt):
        score = Text(f"Your score: {self.player.points}", (self.width // 2, self.height // 2), 30, (255, 255, 0))
        game_over = Text("game over", (self.width // 2, self.height // 2), 96, (255, 255, 0))
        press_key = Text("press any key to continue or enter to play again", (self.width // 2, self.height // 2), 48, (255, 255, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        self.screen.fill("black")

        game_over.draw(self.screen, 50)
        press_key.draw(self.screen, -50)
        score.draw(self.screen, -100)

        self.wait_time += dt
        if self.wait_time > 1.5:
            keys = pygame.key.get_pressed()
            if any(keys) and not keys[pygame.K_RETURN]:
                sys.exit()
            if keys[pygame.K_RETURN]:
                Game().start()
        pygame.display.flip()