import pygame
from Settings import *


class Bin:
    def __init__(self, PositionX, FilePath, Type):
        self.PositionX = PositionX
        self.PositionY = Scale(150)

        self.FilePath = FilePath
        self.Type = Type

        self.Font = pygame.font.Font(None, int(Scale(50)))

        self.Surface = pygame.image.load(self.FilePath).convert_alpha()
        self.Surface = Scale(self.Surface)
        self.Rectangle = self.Surface.get_rect(center = (self.PositionX, self.PositionY))

        self.Labels = []

        for CurrentWordIndex, CurrentWord in enumerate(self.Type.split(" ")):
            Label = self.Font.render(CurrentWord, False, "black")
            Rectangle = Label.get_rect(
                center=(self.PositionX, (self.PositionY + Scale(100)) + (Scale(50) * CurrentWordIndex)))

            self.Labels.append((Label, Rectangle))