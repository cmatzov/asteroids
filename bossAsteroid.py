import random
from asteroid import Asteroid
from constants import *

class Boss(Asteroid):
    def __init__(self, x, y):
        self.radius = ASTEROID_MAX_RADIUS * 3
        super().__init__(x, y, self.radius)
        self.number_of_points = random.randint(20,30)

    @staticmethod
    def spawn(Coordinates):
        speed = random.randint(40, 60)
        position = Coordinates[0][1](random.uniform(0, 1))
        to_player = (Coordinates[1] - position).normalize()
        velocity = to_player * speed
        boss = Boss(position.x, position.y)
        boss.velocity = velocity

    def split(self, screen):
        self.kill()
        angles = [
            random.uniform(10, 30),
            random.uniform(-10, -30),
            random.uniform(-30, -50),
            random.uniform(30, 50)
        ]
        for angle in angles:
            asteroid = Asteroid(self.position.x, self.position.y, ASTEROID_MAX_RADIUS)
            asteroid.velocity = self.velocity.rotate(angle) * 2

    def bounce_away_other(self, other):
        delta = other.position - self.position
        dist = delta.length() or 1
        normal = delta.normalize()
        overlap = (other.radius + self.radius) - dist + 1
        other.position += normal * overlap
        other.velocity = other.velocity.reflect(normal)