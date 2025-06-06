import pygame
import math
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

class Missile(Shot):
    def __init__(self, x, y, asteroids, player_position, player_rotation):
        super().__init__(x, y)
        self.radius = 20
        self.damage = 10
        self.speed = PLAYER_SHOOT_SPEED
        self.asteroids = asteroids
        self.player_position = player_position
        self.player_rotation = player_rotation
        self.image = pygame.image.load("assets/images/missile.png")
        self.image = pygame.transform.smoothscale(self.image, (40, 40))
        self.angle = -player_rotation + 180

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.position)
        self.rect.center = self.position
        screen.blit(rotated_image, self.rect)

    def update(self, dt):
        self.position += (self.velocity * dt)
        if self.position.distance_to(self.player_position) > self.radius * 10:
            for asteroid in self.asteroids:
                if self.position.distance_to(asteroid.position) < asteroid.radius + self.radius * 5:
                    head_towards = (asteroid.position - self.position).normalize()
                    self.velocity = head_towards * self.speed

                    to_target = asteroid.position - self.position
                    target_angle = math.degrees(math.atan2(-to_target.y, to_target.x))

                    angle_diff = (target_angle - self.angle + 90) % 360 - 180
                    max_turn = 200 * dt
                    angle_change = max(-max_turn, min(max_turn, angle_diff))
                    self.angle += angle_change
                    break
        ## Thanks to ChatGPT for this equations and the pngs