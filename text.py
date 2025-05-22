import pygame
from constants import *

class Text():
    def __init__(self, text, position, font_size=36, color=(255, 255, 0)):
        self.text = text
        self.position = position
        self.color = color
        self.font = pygame.font.Font("assets/fonts/star_jedi/starjedi/Starjhol.ttf", font_size)
        self.rendered_text = self.font.render(self.text, True, self.color)

    def draw(self, surface, y):
        self.rect = self.rendered_text.get_rect(center=self.position)
        self.rect.centery -= y
        surface.blit(self.rendered_text, self.rect)

    def update_text(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)