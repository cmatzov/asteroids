import pygame
from powerups import Shield

class Icons():
    def __init__(self, image, position, scale_dimensions):
        self.scale_dimensions = scale_dimensions
        original = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(original, (self.scale_dimensions))
        self.image.set_colorkey("white")
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, (self.position))