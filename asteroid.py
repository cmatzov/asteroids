import pygame
import random
from constants import *
from circleshape import CircleShape
from particles import Particle

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.hits = 0
        self.health = self.radius / 20
        self.rotation = 0
        self.number_of_points = random.randint(12,20)
        self.shape = self.generate_polygon_shape()

    def generate_polygon_shape(self):
        points = []
        for i in range(self.number_of_points):
            angle = i * (360 / self.number_of_points)
            distance = random.uniform(self.radius * 0.8, self.radius)
            point = pygame.Vector2(0, -distance).rotate(angle)
            points.append(point)
        return points

    def draw(self, screen):
        rotated = [p.rotate(self.rotation) for p in self.shape]
        translated = [self.position + p for p in rotated]
        pygame.draw.polygon(screen, (150, 150, 150), translated)

    def update(self, dt):
        self.position += (self.velocity * dt)
    
    @staticmethod
    def spawn(Coordinates):
        speed = random.randint(40, 100)
        velocity = Coordinates[0][0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = Coordinates[0][1](random.uniform(0, 1))
        kind = random.randint(1, ASTEROID_KINDS)
        asteroid = Asteroid(position.x, position.y, ASTEROID_MIN_RADIUS * kind)
        asteroid.velocity = velocity

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        self.radius -= ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, self.radius)
        asteroid.velocity = self.velocity.rotate(random.uniform(20, 50)) * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, self.radius)
        asteroid.velocity = self.velocity.rotate(random.uniform(-20, -50)) * 1.2
    
    def particle_effect(self):
        Particle.spawn(self.position, self.radius, random.randint(10, 100))

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