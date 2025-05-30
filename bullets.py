import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.damage = 1

    def draw(self, screen):
        pygame.draw.circle(screen, (173, 230, 230), self.position, self.radius)

    def update(self, dt):
        self.position += (self.velocity * dt)