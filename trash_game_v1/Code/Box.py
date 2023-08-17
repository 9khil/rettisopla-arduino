import pygame
from Settings import *


class Box:
    def __init__(self, Position, Image, Flash = False):
        self.Position = Position
        self.Image = Image
        self.Flash = Flash

        self.Alpha = 255
        self.AlphaAdd = -5

        self.Surface = pygame.image.load(self.Image).convert_alpha()
        self.Surface = Scale(self.Surface)

        self.Update()

    def Update(self):
        self.Surface.set_alpha(self.Alpha)
        self.Rectangle = self.Surface.get_rect(center = self.Position)

        if self.Flash:
            self.Alpha += self.AlphaAdd

            if self.Alpha >= 255 or self.Alpha <= 30:
                self.AlphaAdd = -self.AlphaAdd