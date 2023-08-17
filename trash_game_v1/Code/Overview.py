import pygame
from Settings import *


class Overview:
    def __init__(self, Name, Position):
        self.Name = Name
        self.Position = Position

        self.Number = 0

        self.Font = pygame.font.Font(None, int(Scale(50)))

        self.Update()

    def Update(self):
        self.Box = pygame.image.load("../Graphics/Score Box.png").convert_alpha()
        self.Box = Scale(self.Box)

        self.Surface = self.Font.render(f"{self.Name}: {self.Number}", False, "white")
        self.Rectangle = self.Surface.get_rect(center = self.Position)

        self.Box.blit(self.Surface, (10, self.Box.get_size()[1] / 4))