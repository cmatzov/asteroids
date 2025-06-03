import pygame
from circleshape import CircleShape
from constants import *
from bullets import Shot
from particles import Trail
from powerups import Shield

class Player(CircleShape):
    def __init__(self, x, y, screen):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = 3
        self.points = 0
        self.player_speed = PLAYER_SPEED
        self.bullet_speed = PLAYER_SHOOT_SPEED
        self.boost_duration = 5
        self.recharging_boost = 0
        self.perks = []
        self.shield = None
        self.screen = screen

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle())

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
        if keys[pygame.K_RETURN]:
            for perk in self.perks:
                print(f"player list {str(self.perks)}")
                if isinstance(perk, Shield):
                    self.perks.remove(perk)
                    self.shield_up()
        if keys[pygame.K_LSHIFT]:
            self.speed_boost(dt)
        else:
            self.player_speed = PLAYER_SPEED

        """ Recharge boost during every update instead of when SHIFT is pressed """
        if self.boost_duration <= 0:
            self.recharging_boost += dt

        if self.shield and self.shield.health == 0:
            self.shield = None

    def shield_up(self):
        self.shield = Shield(self.position, self.screen, is_active=True)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.player_speed * dt
        self.movement_trail(self.position)
    
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
    
    def movement_trail(self, position):
        position1, position2 = self.triangle()[2], self.triangle()[1]
        Trail.spawn(position, position1), Trail.spawn(position, position2)

        """ one point trail
        position1, position2 = self.triangle()[2], self.triangle()[1]
        middle_x, middle_y = (position1[0] + position2[0]) / 2, (position1[1] + position2[1]) / 2
        middle_point = [middle_x, middle_y]
        Trail.spawn(position, middle_point)
        """