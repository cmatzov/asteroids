import pygame
import math
from circleshape import CircleShape

class Shield(CircleShape):
    def __init__(self, center):
        self.radius = 20
        super().__init__(center.x, center.y, self.radius)
        self.color = "white"
        self.size = self.radius * 2
        self.width = 2
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=center)

        self.points = [
            pygame.math.Vector2(self.radius, self.radius) + pygame.math.Vector2(self.radius, 0).rotate(90),
            pygame.math.Vector2(self.radius, self.radius) + pygame.math.Vector2(self.radius, 0).rotate(230),
            pygame.math.Vector2(self.radius, self.radius) + pygame.math.Vector2(self.radius, 0).rotate(310),
        ]
        self.draw()


    def draw(self):
        def draw_arc(p1, p2, bulge=-6):
            mid = (p1 + p2) / 2
            direction = pygame.math.Vector2(-(p2.y - p1.y), p2.x - p1.x).normalize()
            control = mid + direction * bulge

            steps = 30
            last = p1
            for t in range(1, steps + 1):
                alpha = t / steps
                point = (1 - alpha) ** 2 * p1 + 2 * (1 - alpha) * alpha * control + alpha ** 2 * p2
                pygame.draw.line(self.image, self.color, last, point, self.width)
                last = point

        draw_arc(self.points[0], self.points[1])
        draw_arc(self.points[1], self.points[2])
        draw_arc(self.points[2], self.points[0])
    
    def drop_powerup(position):
        Shield(position)

class PlayerShield(pygame.sprite.Sprite):
    def __init__(self, position, screen):
        self.base_radius = 60
        self.radius = self.base_radius
        self.position = position
        self.color = (255, 255, 128)
        self.health = 3
        self.pulse_timer = 0
        self.draw(screen)
    
    def draw(self, screen):
        pulse_amount = 5 * math.sin(self.pulse_timer)
        pulsing_radius = int(self.base_radius + pulse_amount)
        
        pygame.draw.circle(screen, self.color, self.position, pulsing_radius, 6)
        self.pulse_timer += 0.1

    def update(self, player_position):
        self.position = player_position