import pygame
from powerups import Shield

class Icons():
    def __init__(self, image, position, scale_dimensions):
        self.scale_dimensions = scale_dimensions
        original = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(original, (self.scale_dimensions))
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, (self.position))