import random
import pygame
import math
from asteroid import Asteroid
from constants import *

class Boss(Asteroid):
    def __init__(self, x, y):
        self.radius = ASTEROID_MAX_RADIUS * 3
        super().__init__(x, y, self.radius)

    def calculate_angle_to_player(Coordinates):
        dx = Coordinates[1][0] - Coordinates[0][0][0]
        dy = Coordinates[1][1] - Coordinates[0][0][1]
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    @staticmethod
    def spawn(Coordinates):
        speed = random.randint(40, 60)
        velocity = Coordinates[0][0] * speed
        velocity = velocity.rotate(Boss.calculate_angle_to_player(Coordinates))
        position = Coordinates[0][1](random.uniform(0, 1))
        boss = Boss(position.x, position.y)
        boss.velocity = velocity

    def split(self):
        self.kill()
        asteroid = Asteroid(self.position.x, self.position.y, ASTEROID_MAX_RADIUS)
        asteroid.velocity = self.velocity.rotate(random.uniform(10, 30)) * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, ASTEROID_MAX_RADIUS)
        asteroid.velocity = self.velocity.rotate(random.uniform(-10, -30)) * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, ASTEROID_MAX_RADIUS)
        asteroid.velocity = self.velocity.rotate(random.uniform(-30, -50)) * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, ASTEROID_MAX_RADIUS)
        asteroid.velocity = self.velocity.rotate(random.uniform(-30, -50)) * 1.2

    def bounce_away_other(self, other):
        delta = other.position - self.position
        dist = delta.length() or 1
        normal = delta.normalize()

        overlap = (other.radius + self.radius) - dist + 1
        other.position += normal * overlap

        other.velocity = other.velocity.reflect(normal)