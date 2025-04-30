import pygame
import random
from asteroid import Asteroid
from bossAsteroid import Boss
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.boss_timer = 0.0

    def clear(self, CircleShape):
        if (CircleShape.position.x < 0 - ASTEROID_MAX_RADIUS * 4
           or CircleShape.position.x > SCREEN_WIDTH + ASTEROID_MAX_RADIUS * 4
           or CircleShape.position.y < 0 - ASTEROID_MAX_RADIUS * 4
           or CircleShape.position.y > SCREEN_HEIGHT + ASTEROID_MAX_RADIUS * 4):
            CircleShape.kill()

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            asteroid = Asteroid(position.x, position.y, ASTEROID_MIN_RADIUS * kind)
            asteroid.velocity = velocity

        self.boss_timer += dt
        if self.boss_timer > ASTEROID_SPAWN_RATE * 10:
            self.boss_timer = 0

            edge = random.choice(self.edges)
            speed = random.randint(1, 40)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            boss = Boss(position.x, position.y)
            boss.velocity = velocity