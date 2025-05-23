import pygame
from circleshape import CircleShape
from constants import *
from bullets import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = 3
        self.points = 0
        self.player_speed = PLAYER_SPEED
        self.bullet_speed = PLAYER_SHOOT_SPEED
        self.boost_duration = 5
        self.recharging_boost = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_LSHIFT]:
            self.speed_boost(dt)
        else:
            self.player_speed = PLAYER_SPEED

        """ Recharge boost during every update instead of when SHIFT is pressed """
        if self.boost_duration <= 0:
            self.recharging_boost += dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.player_speed * dt
    
    def speed_boost(self, dt):
        self.player_speed = 600
        self.boost_duration -= dt
        if self.boost_duration <= 0:
            self.player_speed = PLAYER_SPEED
            if self.recharging_boost >= 10:
                self.recharging_boost = 0
                self.boost_duration = 5
        """ 
        Boost based on points, define boost_points threshold in constructor

        # self.player_speed = 600
        # self.boost_duration -= dt
        # if self.boost_duration <= 0:
        #     self.player_speed = 200
        #     if self.points >= self.boost_points:
        #         self.boost_points += 50
        #         self.boost_duration = 5

        """


    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.triangle()[0], self.triangle()[0])
        if self.player_speed == 600:
            self.bullet_speed = 800
        else:
            self.bullet_speed = PLAYER_SHOOT_SPEED
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * self.bullet_speed