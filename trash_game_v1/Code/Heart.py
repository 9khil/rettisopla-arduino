import pygame
from Settings import *


class Heart:
    def __init__(self, Position):
        self.Position = Position

        self.Width = Scale(75)
        self.Height = Scale(75)

        self.Enabled = True

        self.Update()

    def Update(self):
        self.HeartContainer = pygame.image.load("../Graphics/Heart Container.png").convert_alpha()
        self.HeartContainer = Scale(self.HeartContainer)

        self.Heart = pygame.image.load("../Graphics/Heart.png").convert_alpha()
        self.Heart = Scale(self.Heart)

        self.Rectangle = self.HeartContainer.get_rect(center=self.Position)
        self.HeartContainer.blit(self.HeartContainer, (0, 0))

        if self.Enabled:
            self.HeartContainer.blit(self.Heart, (0, 0))