import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.hits = 0
        self.max_hits = self.radius / 20
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        self.radius -= ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, self.radius)
        asteroid.velocity = self.velocity.rotate(random.uniform(20, 50)) * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, self.radius)
        asteroid.velocity = self.velocity.rotate(random.uniform(-20, -50)) * 1.2

    def bounce(self, other):
        delta = self.position - other.position
        distance = delta.length()

        if distance == 0:
            delta = pygame.Vector2(1, 0)
            distance = 1

        overlap = 0.5 * (self.radius + other.radius - distance + 1)
        correction = delta.normalize() * overlap

        self.position += correction
        other.position -= correction

        normal = delta.normalize()
        relative_velocity = self.velocity - other.velocity
        speed = relative_velocity.dot(normal)

        if speed > 0:
            return

        impulse = 2 * speed / 2
        self.velocity -= impulse * normal
        other.velocity += impulse * normal


    def update_score(self, radius):
        if radius == 60:
            return 1
        if radius == 20:
            return 10
        if radius == 40:
            return 5
        if radius > 60:
            return 20