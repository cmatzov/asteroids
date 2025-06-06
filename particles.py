import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, position, color, direction, speed, size=2):
        super().__init__(self.containers)
        self.position = pygame.math.Vector2(position)
        self.color = color
        self.direction = direction
        self.speed = speed
        self.lifetime = random.uniform(0.5, 0.55)
        self.age = 0
        self.size = size
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        self.draw()
        self.rect = self.image.get_rect(center=self.position)

    def draw(self):
        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), self.size // 2)

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.center = self.position

        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
    
    @staticmethod
    def spawn(position, offset, n):
        for _ in range(n):
            color = random.choice([(105,105,105), (169,169,169), (211,211,211)])
            direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            spawn_pos = position + direction * offset * 1.2
            speed = random.randint(10, 50)
            Particle(spawn_pos, color, direction, speed)

class Trail(Particle):
    def __init__(self, position, color, direction, speed):
        super().__init__(position, color, direction, speed, size=8)

    @staticmethod
    def spawn(direction, spawn_pos):
        for _ in spawn_pos:
            color = random.choice([(105,105,105), (173, 230, 230), (211,211,211)])
            direction = direction.normalize()
            speed = -100
            Trail(spawn_pos, color, direction, speed)