import pygame
from Settings import *


class Icon:
    def __init__(self, Position, Image):
        self.Position = Position
        self.Image = Image

        self.Size = Scale(250)

        self.Surface = pygame.image.load(self.Image).convert_alpha()

        self.Update()

    def Update(self):
        self.Surface = pygame.transform.scale(self.Surface, (self.Size, self.Size))
        self.Rectangle = self.Surface.get_rect(center = self.Position)