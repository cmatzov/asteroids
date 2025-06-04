import pygame
import math
from circleshape import CircleShape

class Shield(CircleShape):
    def __init__(self, center, screen, is_active=False):
        self.radius = 20
        super().__init__(center.x, center.y, self.radius)
        self.color = "white"
        self.size = self.radius * 2
        self.width = 2
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=center)
        self.is_active = is_active
        self.pulse_timer = 0
        self.active_radius = 60
        self.position = center
        self.health = 3
        self.screen = screen

        self.points = [
            pygame.math.Vector2(self.radius, self.radius) + pygame.math.Vector2(self.radius, 0).rotate(90),
            pygame.math.Vector2(self.radius, self.radius) + pygame.math.Vector2(self.radius, 0).rotate(230),
            pygame.math.Vector2(self.radius, self.radius) + pygame.math.Vector2(self.radius, 0).rotate(310),
        ]
        self.draw()

    def __repr__(self):
        return "Shield"

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
        if self.is_active == False:
            draw_arc(self.points[0], self.points[1])
            draw_arc(self.points[1], self.points[2])
            draw_arc(self.points[2], self.points[0])
        if self.is_active == True:
            self.color = (255, 255, 128)
            self.pulse_timer += 0.1
            pulse_amount = 5 * math.sin(self.pulse_timer)
            pulsing_radius = int(self.active_radius + pulse_amount)
            pygame.draw.circle(self.screen, self.color, self.position, pulsing_radius, 6)

    def update(self, player_position):
        if self.is_active == True:
            self.position = player_position
            self.pulse_timer += 0.1
            pulse_amount = 5 * math.sin(self.pulse_timer)
            pulsing_radius = int(self.active_radius + pulse_amount)
            self.radius = pulsing_radius
            self.rect.center = self.position
    
    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

class BonusLife(CircleShape):
    def __init__(self, center):
        self.radius = 20
        super().__init__(center.x, center.y, self.radius)
        self.color = "red"
        self.heart_scale = 1
        self.surface_size = self.heart_scale * 32
        self.image = pygame.Surface((self.surface_size, self.surface_size)).convert_alpha()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=center)
        self.position = center
        self.is_active = False

    def draw(self):
        points = []
        point_count=100
        for i in range(point_count):
            t = math.pi * 2 * i / point_count
            x = 16 * math.sin(t)**3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            x *= self.heart_scale
            y *= -self.heart_scale
            x += self.image.get_width() // 2
            y += self.image.get_height() // 2
            points.append((x, y))
        pygame.draw.polygon(self.image, self.color, points)