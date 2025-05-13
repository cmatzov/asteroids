import pygame
import random
from constants import *
from dataclasses import dataclass

@dataclass
class Coordinates():
    def __init__(self, edge, player_position):
        self.edge = edge
        self.player_position = player_position
    
    def coordinates(self):
        return self.edge, self.player_position

class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, player_position, width, height):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = ASTEROID_SPAWN_RATE
        self.player_position = player_position
        self.edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * height),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                width + ASTEROID_MAX_RADIUS, y * height
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * width, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * width, height + ASTEROID_MAX_RADIUS
            ),
        ],
    ]
    
    def update(self, player_moved):
        self.player_position = player_moved

    def clear(self, CircleShape, width, height):
        if (CircleShape.position.x < 0 - ASTEROID_MAX_RADIUS * 4
           or CircleShape.position.x > width + ASTEROID_MAX_RADIUS * 4
           or CircleShape.position.y < 0 - ASTEROID_MAX_RADIUS * 4
           or CircleShape.position.y > height + ASTEROID_MAX_RADIUS * 4):
            CircleShape.kill()

    def spawn(self, dt, CircleShape, ignore_timer=False):
        edge = random.choice(self.edges)
        spawn_point = Coordinates(edge, self.player_position)
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE or ignore_timer == True:
            CircleShape.spawn(spawn_point.coordinates())
            self.spawn_timer = 0.0